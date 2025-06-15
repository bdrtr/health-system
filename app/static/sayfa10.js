document.addEventListener("DOMContentLoaded", () => {
    const updateBtn = document.querySelector(".updateBtn");
    const logoutBtn = document.querySelector(".logoutBtn");
  
    updateBtn.addEventListener("click", () => {
      const newPass = document.querySelectorAll("input[type='password']")[0].value;
      const confirmPass = document.querySelectorAll("input[type='password']")[1].value;
  
      if (newPass.length < 6) {
        alert("Şifre en az 6 karakter olmalı.");
      } else if (newPass !== confirmPass) {
        alert("Şifreler uyuşmuyor.");
      } else {
        // Burada backend'e istek gönderilebilir (API)
        alert("Şifreniz başarıyla güncellendi.");
        // şifreyi boşalt
        document.querySelectorAll("input[type='password']").forEach(input => input.value = "");
      }
    });
  
    logoutBtn.addEventListener("click", () => {
      // Gerçek sistemde oturumu sonlandırmak gerekir (örneğin token silmek)
      alert("Çıkış yapıldı.");
      window.location.href = "login.html"; // giriş sayfasına yönlendir
    });
  });
  