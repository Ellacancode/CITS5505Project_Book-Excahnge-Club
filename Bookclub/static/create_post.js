// image preview function
document.getElementById('imageUpload').addEventListener('change', function(event) {
    var output = document.getElementById('imagePreview');
    output.style.display = 'block';
    output.src = URL.createObjectURL(event.target.files[0]);
    output.onload = function() {
        URL.revokeObjectURL(output.src)
    }
});