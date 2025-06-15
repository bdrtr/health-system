document.getElementById("registerForm").addEventListener("submit", function (e) {
    e.preventDefault();
  
    const fullname = document.getElementById("fullname").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;
    const errorDiv = document.getElementById("errorMsg");
  
    if (!fullname || !email || !password || !confirmPassword) {
      errorDiv.textContent = "Lütfen tüm alanları doldurun.";
      return;
    }
  
    if (password !== confirmPassword) {
      errorDiv.textContent = "Şifreler eşleşmiyor.";
      return;
    }
  
    errorDiv.textContent = "";
    alert("Kayıt başarıyla tamamlandı. Giriş sayfasına yönlendiriliyorsunuz.");
    window.location.href = "sayfa1.html";
  });
  