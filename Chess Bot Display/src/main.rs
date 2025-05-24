use std::io::Cursor;

use image::codecs::png::PngEncoder;
use image::{ColorType, GenericImageView, ImageBuffer, ImageEncoder, Rgba};
use pyo3::types::{IntoPyDict, PyBytes, PyList};
use pyo3::{prelude::*, py_run};

use raqote::{DrawOptions, DrawTarget, LineJoin, PathBuilder, SolidSource, Source, StrokeStyle};

// fn vec_u8_to_png_buffer(
//     raw_pixels: Vec<u8>,
//     width: u32,
//     height: u32,
//     color_type: ColorType,
// ) -> Result<Vec<u8>, Box<dyn std::error::Error>> {
//     // Create a buffer to write PNG into
//     let mut png_buffer = Cursor::new(Vec::new());

//     // Choose a PNG encoder
//     let encoder = image::codecs::png::PngEncoder::new(&mut png_buffer);

//     // Encode the image
//     encoder.encode(&raw_pixels, width, height, color_type)?;

//     // Return the internal buffer (now containing PNG bytes)
//     Ok(png_buffer.into_inner())
// }

fn main() -> anyhow::Result<()> {
    let mut base_image = image::open("output/monitor_1.png")?;

    Python::with_gil(|py| {
        let img_data = image::open("output/monitor_1.png")?;
        let (image_width, image_height) = img_data.dimensions();

        let byte_array = img_data.to_rgba8().into_raw();

        let mut buffer = Cursor::new(Vec::new());
        let encoder = PngEncoder::new(&mut buffer);

        encoder.write_image(
            &byte_array,
            image_width,
            image_height,
            ColorType::Rgba8.into(),
        )?;

        let png_buffer = buffer.into_inner();

        let pil = PyModule::import(py, "PIL.Image")?;
        let io = PyModule::import(py, "io")?;
        let ultralytics = PyModule::import(py, "ultralytics")?;

        let model = ultralytics
            .getattr("YOLO")?
            .call1(("../assets/best.onnx",))?;

        let py_bytes = PyBytes::new(py, &png_buffer);
        let io_buffer = io.call_method1("BytesIO", (py_bytes,))?;

        let pil_img = pil.call_method1("open", (io_buffer,))?;

        let start_time = std::time::Instant::now();

        // Step 5: Run prediction
        let kwargs = [("source", pil_img)].into_py_dict(py)?;
        let result = model
            .call_method("predict", (), Some(&kwargs))?
            .get_item(0)?;

        println!("Prediction results: {:?}", result);

        let boxes = result.getattr("boxes")?;
        let xyxy = boxes.getattr("xyxy")?; // Tensor of shape (N, 4)
        let cls_ids = boxes.getattr("cls")?; // Tensor of shape (N,)

        // Convert tensors to Python lists (optionally NumPy if needed)
        let binding = xyxy.call_method0("tolist")?;
        let xyxy_list = binding
            .downcast::<PyList>()
            .map_err(|e| anyhow::anyhow!("xyxy downcast failed: {e}"))?;

        let binding = cls_ids.call_method0("tolist")?;
        let cls_list = binding
            .downcast::<PyList>()
            .map_err(|e| anyhow::anyhow!("cls_ids downcast failed: {e}"))?;

        let conf_list = boxes.getattr("conf")?.call_method0("tolist")?;
        let conf_list = conf_list
            .downcast::<PyList>()
            .map_err(|e| anyhow::anyhow!("conf_list downcast failed: {e}"))?;

        // Get class name mapping from the model
        let names = model.getattr("names")?; // dict: class_id -> class_name

        println!("Took {} ms", start_time.elapsed().as_millis());

        let mut dt = DrawTarget::new(image_width as _, image_height as _);

        // Iterate through detections
        for (i, bbox) in xyxy_list.iter().enumerate() {
            let cls_id = cls_list.get_item(i)?;
            let class_name = names.get_item(cls_id)?;
            let confidence = conf_list.get_item(i)?.extract::<f32>()?;
            let bbox_values = bbox.extract::<[f32; 4]>()?;

            if confidence < 0.9 {
                continue; // Skip low-confidence detections
            }
            println!(
                "Detection {}: box = {:?}, confidence = {}",
                i, bbox_values, confidence
            );

            let (x1, y1, x2, y2) = (
                bbox_values[0] as f32,
                bbox_values[1] as f32,
                bbox_values[2] as f32,
                bbox_values[3] as f32,
            );

            // for (bbox, label, _confidence) in result {
            let mut pb = PathBuilder::new();
            pb.rect(x1, y1, x2 - x1, y2 - y1);
            let path = pb.finish();

            let color = SolidSource {
                r: 0x80,
                g: 0x10,
                b: 0x40,
                a: 0x80,
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
            ImageBuffer::from_raw(image_width, image_height, dt.get_data_u8().to_vec()).unwrap();
        let overlay = image::DynamicImage::ImageRgba8(image_buffer).to_rgba8();

        image::imageops::overlay(&mut base_image, &overlay, 0, 0);

        base_image.save("stages/overlay.png").unwrap();

        Ok(())
    })
}
