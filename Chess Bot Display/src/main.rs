use std::path::Path;

use image::{GenericImageView, ImageBuffer, Rgb, Rgba, imageops::FilterType};
use ndarray::{Array, Axis, s};
use ort::{
    inputs,
    session::{Session, SessionOutputs},
    value::{Tensor, TensorRef},
};
use raqote::{DrawOptions, DrawTarget, LineJoin, PathBuilder, SolidSource, Source, StrokeStyle};
use show_image::{AsImageView, Image, WindowOptions, event};
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

#[derive(Debug, Clone, Copy)]
struct BoundingBox {
    x1: f32,
    y1: f32,
    x2: f32,
    y2: f32,
}

fn intersection(box1: &BoundingBox, box2: &BoundingBox) -> f32 {
    (box1.x2.min(box2.x2) - box1.x1.max(box2.x1)) * (box1.y2.min(box2.y2) - box1.y1.max(box2.y1))
}

fn union(box1: &BoundingBox, box2: &BoundingBox) -> f32 {
    ((box1.x2 - box1.x1) * (box1.y2 - box1.y1)) + ((box2.x2 - box2.x1) * (box2.y2 - box2.y1))
        - intersection(box1, box2)
}

// #[rustfmt::skip]
// const YOLOV8_CLASS_LABELS: [&str; 13] = [
//     "king", "queen", "rook", "bishop", "knight", "pawn",
//     "king", "queen", "rook", "bishop", "knight", "pawn",
//     "board"
// ];

const YOLOV8_CLASS_LABELS: [&str; 13] = [
    "K", "Q", "R", "B", "N", "P", "k", "q", "r", "b", "n", "p", "board",
];

#[show_image::main]
fn main() -> anyhow::Result<()> {
    // Initialize tracing to receive debug messages from `ort`
    // tracing_subscriber::registry()
    // 	.with(tracing_subscriber::EnvFilter::try_from_default_env().unwrap_or_else(|_| "info,ort=debug".into()))
    // 	.with(tracing_subscriber::fmt::layer())
    // 	.init();

    let current_dir = std::env::current_dir()?;

    let original_img = image::open(current_dir.join("test_image.png")).unwrap();
    let (img_width, img_height) = (original_img.width(), original_img.height());

    let img = original_img.resize_exact(640, 640, FilterType::CatmullRom);

    let mut input = Array::zeros((1, 3, 640, 640));

    for pixel in img.pixels() {
        let x = pixel.0 as _;
        let y = pixel.1 as _;
        let [r, g, b, _] = pixel.2.0;
        input[[0, 0, y, x]] = (r as f32) / 255.;
        input[[0, 1, y, x]] = (g as f32) / 255.;
        input[[0, 2, y, x]] = (b as f32) / 255.;
    }

    // Save the resized image for debugging
    img.save(current_dir.join("stages/resized_image.png"))
        .unwrap();

    let assets_folder = current_dir.parent().unwrap().join("assets");
    let model_path = assets_folder.join("best.onnx");

    println!("Loading model from path: {:?}", model_path);

    let model = Session::builder()?.commit_from_file(model_path)?;
    let tensor = Tensor::from_array(input)?;

    let inputs = inputs!["images" => tensor]?;
    let outputs: SessionOutputs = model.run(inputs)?;

    println!("Output: {:?}", outputs);

    let ouput = &outputs["output0"];
    let output = ouput.try_extract_tensor::<f32>()?.reversed_axes();

    // println!("Output shape: {:?}", output.shape());
    // println!("Output data: {:?}", output);

    let mut boxes = Vec::new();
    let output = output.slice(s![.., .., 0]);

    for row in output.axis_iter(Axis(0)) {
        let row: Vec<_> = row.iter().copied().collect();

        let (class_id, prob) = row
            .iter()
            // skip bounding box coordinates
            .skip(4)
            .enumerate()
            .map(|(index, value)| (index, *value))
            .reduce(|accum, row| if row.1 > accum.1 { row } else { accum })
            .unwrap();

        // if prob < 0.3 {
        //     continue;
        // }
        let label = YOLOV8_CLASS_LABELS[class_id];

        let xc = row[0] / 640. * (img_width as f32);
        let yc = row[1] / 640. * (img_height as f32);
        let w = row[2] / 640. * (img_width as f32);
        let h = row[3] / 640. * (img_height as f32);

        boxes.push((
            BoundingBox {
                x1: xc - w / 2.,
                y1: yc - h / 2.,
                x2: xc + w / 2.,
                y2: yc + h / 2.,
            },
            label,
            prob,
        ));

        println!("Class Name: {}, Probability: {}", YOLOV8_CLASS_LABELS[class_id], prob);
    }

    boxes.sort_by(|box1, box2| box2.2.total_cmp(&box1.2));

    // println!("Boxes: {:?}", boxes);

    let mut result = Vec::new();
    while !boxes.is_empty() {
        result.push(boxes[0]);
        boxes = boxes
            .iter()
            .filter(|box1| intersection(&boxes[0].0, &box1.0) / union(&boxes[0].0, &box1.0) < 0.7)
            .copied()
            .collect();
    }

    println!("Filtered Boxes: {:#?}", result);

    let mut dt = DrawTarget::new(img_width as _, img_height as _);

    for (bbox, label, _confidence) in result {
        let mut pb = PathBuilder::new();
        pb.rect(bbox.x1, bbox.y1, bbox.x2 - bbox.x1, bbox.y2 - bbox.y1);
        let path = pb.finish();

        let color = match label {
            _ => SolidSource {
                r: 0x80,
                g: 0x10,
                b: 0x40,
                a: 0x80,
            },
        };
        dt.stroke(
            &path,
            &Source::Solid(color),
            &StrokeStyle {
                join: LineJoin::Round,
                width: 4.,
                ..StrokeStyle::default()
            },
            &DrawOptions::new(),
        );
    }

    let image_buffer: ImageBuffer<Rgba<u8>, Vec<u8>> =
        ImageBuffer::from_raw(img_width, img_height, dt.get_data_u8().to_vec()).unwrap();
    let overlay = image::DynamicImage::ImageRgba8(image_buffer).to_rgba8();

    let mut base_image = original_img.clone();
    image::imageops::overlay(&mut base_image, &overlay, 0, 0);

    base_image
        .save(current_dir.join("stages/overlay.png"))
        .unwrap();

    // let output_path = current_dir.join("output.png");
    // let data = dt.get_data_u8();
    // let image: ImageBuffer<Rgb<u8>, _> = ImageBuffer::from_raw(img_width, img_height, data).unwrap();

    // image.save(&output_path).unwrap();

    println!("Output saved");

    Ok(())
}
