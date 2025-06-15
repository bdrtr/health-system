// Yeni kullanıcı eklemek için formu işleme
document.getElementById('addUserForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Formun sayfayı yeniden yüklemesini engelle
  
    // Form verilerini al
    const name = document.getElementById('name').value;
    const role = document.getElementById('role').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
  
    // Burada kullanıcı verilerini servera göndererek kaydedebilirsiniz.
    // Örnek olarak konsola yazdırıyoruz
    console.log(`Yeni Kullanıcı: ${name}, Rol: ${role}, E-posta: ${email}, Şifre: ${password}`);
  
    // Kullanıcıyı ekledikten sonra, sayfa11'e geri yönlendir
    alert("Yeni kullanıcı başarıyla eklendi!");
    window.location.href = 'sayfa11.html'; // Yönlendirme yapılacak sayfa
  });
  