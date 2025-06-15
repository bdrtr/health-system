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
  
    // Burada gerçek veri kaydını yapmalısınız. (API çağrısı vs.)
    
    // Kullanıcıyı ekledikten sonra, başarı mesajını göster
    alert("Yeni kullanıcı başarıyla eklendi!");
  
    // "Tamam" butonuna basıldığında sayfa11.html'e yönlendir
    window.location.href = 'sayfa11.html'; // Yönlendirme yapılacak sayfa
  });
  