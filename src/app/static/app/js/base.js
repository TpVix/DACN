
let currentImageIndex = 0;
const images = document.querySelectorAll('#banner img');
const links = document.querySelectorAll('#banner a');
const totalImages = images.length;

function showImage(index) {
    images.forEach((img, i) => {
        if (i === index) {
            img.style.display = 'block';
        } else {
            img.style.display = 'none';
        }
    });
}
function changeImage() {
    currentImageIndex = (currentImageIndex + 1) % totalImages;
    showImage(currentImageIndex);

    // Thay đổi href của thẻ a tương ứng với hình ảnh
//    links.forEach((link, i) => {
//     if (i === currentImageIndex) {
//         if (currentImageIndex === 0) {
//             link.setAttribute('href', 'product_detail/1/');
//         } else if (currentImageIndex === 1) {
//             link.setAttribute('href', 'product_detail/12/');
//         } 
//     }
// });

}
setInterval(changeImage, 3000);
showImage(currentImageIndex);
