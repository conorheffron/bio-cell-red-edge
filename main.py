import skimage as ski
import matplotlib.pyplot as plt
from scipy import ndimage as ndi

if __name__ == '__main__':
    path = "/Users/conorheffron/Library/CloudStorage/GoogleDrive-conor.heffron@ucdconnect.ie/My Drive/UCD/MSc in AI for Medicine and Medical Research/Courses/Trimester 1/ANAT40040-Bio Principles & Cellular Org/self assessment/reflective piece 1/"
    cells_image = ski.io.imread(path + "original image cropped.png")[:,:,:3]

    grayscale = ski.color.rgb2gray(cells_image)

    sobel_edge = ski.filters.roberts(grayscale)
    thresh = ski.filters.threshold_triangle(sobel_edge)

    red_noise = ski.restoration.denoise_tv_chambolle(sobel_edge, weight=0.01, channel_axis=-1)

    binary = thresh < red_noise

    fill = ndi.binary_fill_holes(binary)

    dilate = ski.morphology.binary_dilation(fill)

    overlay = ski.color.label2rgb(dilate, image=cells_image, bg_label=0)

    fig, axes = plt.subplots(4, 2)

    axes[0, 0].imshow(cells_image)
    axes[0, 0].set_title('1. Original')

    axes[0, 1].imshow(grayscale, cmap=plt.cm.gray)
    axes[0, 1].set_title('2. Grayscale')

    axes[1, 0].imshow(sobel_edge, cmap=plt.cm.gray)
    axes[1, 0].set_title('3. Sobel Edge Detection')

    axes[1, 1].imshow(red_noise, cmap=plt.cm.gray)
    axes[1, 1].set_title('4. Reduce Noise')

    axes[2, 0].imshow(binary, cmap=plt.cm.gray)
    axes[2, 0].set_title('5. Binary')

    axes[2, 1].imshow(fill, cmap=plt.cm.gray)
    axes[2, 1].set_title('6. Fill Gaps')

    axes[3, 0].imshow(dilate, cmap=plt.cm.gray)
    axes[3, 0].set_title('7. Dilate Image')

    axes[3, 1].imshow(overlay, cmap=plt.cm.gray)
    axes[3, 1].set_title('8. Overlay Original Image with Segmented Cells From Dilated Image')

    plt.tight_layout()
    plt.savefig('result.png')
    plt.show()