onUiLoaded(() => {
    addUploadButton('txt2img');
    addUploadButton('img2img');
    addUploadButton('extras');
});

function addUploadButton(type) {
    let uploadButton = gradioApp().querySelector(`#${type}_upload`);
    const parent = gradioApp().querySelector(`#image_buttons_${type}`);
    if (uploadButton || !parent)
        return;
    uploadButton = createUploadButton(`${type}_upload`, type);
    parent.appendChild(uploadButton);
}

function createUploadButton(id, type) {
    const button = document.createElement('button');
    button.id = id;
    button.type = 'button';
    button.innerText = 'Upload'
    button.className = 'lg secondary gradio-button svelte-1ipelgc';
    button.addEventListener('click', () => uploadCurrentImage(type));
    return button;
}

function uploadCurrentImage(type) {
    const currentImage = gradioApp().querySelector(`#${type}_gallery > .preview > img`);
    if (!currentImage || !currentImage.src) {
        console.log('No image selected.');
        return;
    }
    const matches = currentImage.src.match(/.+\/([^?]+).*/);
    if (matches.length < 2) {
        console.log('Can not parse image path: ' + currentImage.src);
        return;
    }
    const name = matches[1];
    fetch('/image-upload/' + type + '/' + name, {
        method: "POST"
    })
    .then(data => console.log('Image Upload: ' + data.statusText));
}
