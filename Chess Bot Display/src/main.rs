// use fs_extra::dir;
use std::{fs::create_dir_all, time::Instant};
use xcap::{image::{DynamicImage, RgbaImage}, Monitor};
use yolo_rs::{image_to_yolo_input_tensor, model::YoloModelSession};
use ort::ExecutionProvider;


fn normalized(filename: String) -> String {
    filename.replace(['|', '\\', ':', '/'], "")
}

fn main() {
    let start = Instant::now();
    let monitors = Monitor::all().unwrap();

    create_dir_all("./target/monitors").unwrap();

    let monitor_images = 
        monitors
            .iter()
            .map(|monitor| monitor.capture_image().unwrap())
            .collect::<Vec<RgbaImage>>();

    // let onnxSession = 

    let absoltuePath = std::env::current_dir().unwrap();
    let onnxPath = format!("{}/yolov8m.onnx", absoltuePath.display());

    println!("onnxPath {:?}", onnxPath);

    let yoloSession = YoloModelSession::from_filename_v8(onnxPath).unwrap();
    println!("Yolo session loaded {:?}", yoloSession.get_labels());
    
    for image in monitor_images.iter() {
        let dynamicImage = DynamicImage::ImageRgba8(image.clone());

        let yolo_input = image_to_yolo_input_tensor(&dynamicImage);
        // let output = yolo_rs::inference("./yolo11npt", yolo_input);


    }


    println!("Taken {:?}", start.elapsed());
    
}
