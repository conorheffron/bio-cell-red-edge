import skimage as ski
import matplotlib.pyplot as plt
from scipy import ndimage as ndi
import sys, os


def process_cell_image(cells_image):
    binary, dilate, fill, grayscale, overlay, red_noise, sobel_edge = build_output_image(cells_image)

    # configure layout and save result
    set_result_image_layout(binary, cells_image, dilate, fill, grayscale, overlay, red_noise, sobel_edge)


def set_result_image_layout(binary, cells_image, dilate, fill, grayscale, overlay, red_noise, sobel_edge):
    fig, axes = plt.subplots(4, 2)
    print("Set original image to output")
    axes[0, 0].imshow(cells_image)
    axes[0, 0].set_title('1. Original')
    print("Set gray scale image to output")
    axes[0, 1].imshow(grayscale, cmap=plt.cm.gray)
    axes[0, 1].set_title('2. Grayscale')
    print("Set Sobel Edge detection image to output")
    axes[1, 0].imshow(sobel_edge, cmap=plt.cm.gray)
    axes[1, 0].set_title('3. Sobel Edge Detection')
    print("Set noise reduction image to output")
    axes[1, 1].imshow(red_noise, cmap=plt.cm.gray)
    axes[1, 1].set_title('4. Reduce Noise')
    print("Set binary image to output")
    axes[2, 0].imshow(binary, cmap=plt.cm.gray)
    axes[2, 0].set_title('5. Binary')
    print("Set gap fill image to output")
    axes[2, 1].imshow(fill, cmap=plt.cm.gray)
    axes[2, 1].set_title('6. Fill Gaps')
    print("Set dilated image to output")
    axes[3, 0].imshow(dilate, cmap=plt.cm.gray)
    axes[3, 0].set_title('7. Dilate Image')
    print("Set overlay / final image to output")
    axes[3, 1].imshow(overlay, cmap=plt.cm.gray)
    axes[3, 1].set_title('8. Overlay Original Image with Segmented Cells From Dilated Image')

    plt.tight_layout()
    output_file_name = 'result.png'
    plt.savefig(output_file_name)
    print("Image processing complete, please see results at: %s" % os.path.join(os.getcwd(), output_file_name))
    plt.show()


def build_output_image(cells_image):
    grayscale = ski.color.rgb2gray(cells_image)
    sobel_edge = ski.filters.roberts(grayscale)
    thresh = ski.filters.threshold_triangle(sobel_edge)
    red_noise = ski.restoration.denoise_tv_chambolle(sobel_edge, weight=0.01, channel_axis=-1)
    binary = thresh < red_noise
    fill = ndi.binary_fill_holes(binary)
    dilate = ski.morphology.binary_dilation(fill)
    overlay = ski.color.label2rgb(dilate, image=cells_image, bg_label=0)
    return binary, dilate, fill, grayscale, overlay, red_noise, sobel_edge


if __name__ == '__main__':
    print("The name of the program is: %s" % sys.argv[0])

    file_path = str(sys.argv[1])
    print("The file for processing is located at: %s" % file_path)

    cells_image = ski.io.imread(file_path)[:,:,:3]

    process_cell_image(cells_image)