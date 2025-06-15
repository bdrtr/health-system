// Röntgen dosyasını yüklerken önizleme ve dosya kontrolü
document.getElementById("fileInput").addEventListener("change", function (e) {
    const file = e.target.files[0];
    const imagePreview = document.getElementById("imagePreview");
    const errorMessage = document.getElementById("errorMessage");
  
    // Yalnızca görüntü dosyalarını kabul et
    if (file && file.type.startsWith("image/")) {
      const reader = new FileReader();
      
      reader.onload = function (event) {
        imagePreview.src = event.target.result;
        imagePreview.style.display = "block";
        errorMessage.style.display = "none"; // Hata mesajını gizle
      };
      
      reader.readAsDataURL(file);
    } else {
      imagePreview.style.display = "none";
      errorMessage.style.display = "block"; // Hata mesajını göster
    }
  });
  
  // Yükleme butonuna basıldığında
  document.getElementById("xrayUploadForm").addEventListener("submit", async function (e) {
    e.preventDefault();
  
    const form = e.target;
    const formData = new FormData(form);
    
    // Yükleme mesajını göster
    document.getElementById("uploadMessage").style.display = "block";
  
    try {
      // Burada yüklemeyi gerçekleştirecek API'yi çağırıyoruz (örneğin)
      const response = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
      });
  
      const result = await response.json();
  
      if (response.ok) {
        alert("Röntgen başarıyla yüklendi!");
      } else {
        alert("Yükleme başarısız oldu: " + result.detail);
      }
    } catch (err) {
      alert("Sunucuya bağlanılamadı: " + err.message);
    }
  });
  