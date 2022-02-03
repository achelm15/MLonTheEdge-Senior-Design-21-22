import tflite_runtime.interpreter as tflite
import PIL
import PIL.Image
import datetime


def process_image(img):
    """Resize, reduce and expand image.

    # Argument:
        img: original image.

    # Returns
        image: ndarray(64, 64, 3), processed image.
    """
    image = np.array(img.resize((416, 416)), dtype="int8")
    #     image /= 255.
    image = np.expand_dims(image, axis=0)

    return image


model_path = "test.tflite"
interpreter = tflite.Interpreter(model_path)
interpreter = tflite.Interpreter(
    model_path, experimental_delegates=[tflite.load_delegate("libedgetpu.so.1")]
)
print(type(interpreter))

interpreter.allocate_tensors()
image = "test.jpg"
pimage = process_image(Image.open(image))
print(pimage)
image = Image.open(image)
input_index = interpreter.get_input_details()[0]["index"]
output_index = interpreter.get_output_details()[0]["index"]
interpreter.set_tensor(input_index, np.array(pimage))
start = datetime.datetime.now()
interpreter.invoke()
print(datetime.datetime.now() - start)
outs = interpreter.get_tensor(output_index)
shape = np.array(pimage).shape
outs = [np.array(outs)]
image = np.array(image)
print(image.shape)