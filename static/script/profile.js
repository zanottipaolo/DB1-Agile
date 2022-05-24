/* Preview new img account on load */
avatar_upload.onchange = evt => {
    const [file] = avatar_upload.files
    if (file) {
      avatar_img.src = URL.createObjectURL(file)
    }
}