document.getElementById('roleSelect').addEventListener('change', function () {
    let role = this.value;
    let roleOptions = document.getElementById('roleOptions');
    let errorMsg = document.getElementById('errorMsg');
    
    // Temizle
    roleOptions.innerHTML = '';
    errorMsg.textContent = '';
  
    if (role === 'hasta') {
      roleOptions.innerHTML = `
        <button>Röntgen Yükle</button>
        <button>Raporlarım</button>
        <button>Randevu Al</button>
        <button>Profilim</button>
      `;
    } else if (role === 'doktor') {
      roleOptions.innerHTML = `
        <button>Hastalarım</button>
        <button>Randevular</button>
        <button>Rapor İncele</button>
        <button>Profilim</button>
      `;
    } else if (role === 'admin') {
      roleOptions.innerHTML = `
        <button>Kullanıcı Yönetimi</button>
        <button>Sistem Logları</button>
        <button>Raporlar</button>
      `;
    } else {
      errorMsg.textContent = 'Geçersiz rol seçildi!';
    }
  });
  