// use fs_extra::dir;
use arcstr::ArcStr;
use ort::ExecutionProvider;
use std::{fs::create_dir_all, time::Instant};
use xcap::{
    Monitor,
    image::{DynamicImage},
};
use yolo_rs::{image_to_yolo_input_tensor, model::YoloModelSession, YoloEntityOutput};
use image::{Rgba, RgbaImage};
use imageproc::drawing::{draw_hollow_rect_mut, draw_text_mut};
use imageproc::rect::Rect;
use rusttype::{Font, Scale};
use ab_glyph::{FontArc};


fn normalized(filename: String) -> String {
    filename.replace(['|', '\\', ':', '/'], "")
}


/// Draw bounding boxes and labels on an image
fn draw_detections(
    image: &mut RgbaImage,
    detections: &[YoloEntityOutput],
    font_path: &str,
) {
    let font = FontArc::try_from_slice(include_bytes!("Roboto-Regular.ttf")).unwrap();


    let red = Rgba([255u8, 0u8, 0u8, 255u8]);

    for det in detections {
        let rect = Rect::at(det.bounding_box.x1 as i32, det.bounding_box.y1 as i32)
            .of_size(
                (det.bounding_box.x2 - det.bounding_box.x1) as u32,
                (det.bounding_box.y2 - det.bounding_box.y1) as u32,
            );

        // Draw bounding box
        draw_hollow_rect_mut(image, rect, red);

        // Draw label with confidence
        let label = format!("{} {:.2}", det.label, det.confidence);
        // let scale = Scale::uniform(20.0);

        draw_text_mut(image, red, rect.left(), rect.top() - 22, 20.0, &font, &label);
    }
}

fn main() -> anyhow::Result<()> {
    let start = Instant::now();
    let monitors = Monitor::all().unwrap();

    // let font_data = include_bytes!("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf");
    // let font = Font::try_from_bytes(font_data as &[u8]).unwrap();

    create_dir_all("./target/monitors").unwrap();

    let monitor_images = monitors
        .iter()
        .map(|monitor| monitor.capture_image().unwrap())
        .collect::<Vec<RgbaImage>>();

    let current_dir = std::env::current_dir().unwrap();
    let onnx_path = current_dir.parent().unwrap().join("assets/best.onnx");

    println!("Using onnx @ {:?}", onnx_path);

    let mut yolo_session = YoloModelSession::from_filename_v8(onnx_path).unwrap();

    // For some reason, the model is not loaded with the correct labels
    yolo_session.labels = vec![
        "K", "Q", "R", "B", "N", "P", // White pieces
        "k", "q", "r", "b", "n", "p",     // Black pieces
        "board", // Board class
    ]
    .iter()
    .map(|&label| ArcStr::from(label))
    .collect();

    println!("Yolo session loaded {:?}", yolo_session.get_labels());

    for (i, image) in monitor_images.iter().enumerate() {
        let dynamic_image = DynamicImage::ImageRgba8(image.clone());
        let yolo_input = image_to_yolo_input_tensor(&dynamic_image);

        let output = yolo_rs::inference(&yolo_session, yolo_input.view())?;
        // let output = yolo_session.postprocess(output, 0.5).unwrap();

        // println!("Output: {:#?}", output);

        let mut image_with_boxes = image.clone(); // Mutable image for drawing
        draw_detections(&mut image_with_boxes, &output, "./Roboto-Regular.ttf");
    
        // Save or display the image
        let output_path = format!("./output/monitor_{}.png", i);
        image::save_buffer_with_format(
            &output_path,
            &image_with_boxes,
            image_with_boxes.width(),
            image_with_boxes.height(),
            image::ColorType::Rgba8,
            image::ImageFormat::Png,
        )?;
    }

    println!("Taken {:?}", start.elapsed());

    Ok(())
}
