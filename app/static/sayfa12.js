document.addEventListener("DOMContentLoaded", () => {
    const activitiesTable = document.querySelector("#activitiesTable tbody");
    const logsTable = document.querySelector("#logsTable tbody");
  
    // Örnek kullanıcı aktiviteleri
    const activities = [
      { user: 'Emre Yılmaz', activity: 'Giriş yaptı', date: '2025-05-01 12:00' },
      { user: 'Ali Can', activity: 'Röntgen yükledi', date: '2025-05-01 12:30' },
      { user: 'Zeynep Kara', activity: 'Teşhis yaptı', date: '2025-05-01 13:00' },
    ];
  
    // Örnek sistem logları
    const logs = [
      { logId: '1', message: 'Veritabanı yedeği alındı', date: '2025-05-01 11:59' },
      { logId: '2', message: 'API hatası - Sunucu kapalı', date: '2025-05-01 12:05' },
    ];
  
    // Tabloyu doldur
    activities.forEach(activity => {
      activitiesTable.innerHTML += `
        <tr>
          <td>${activity.user}</td>
          <td>${activity.activity}</td>
          <td>${activity.date}</td>
        </tr>
      `;
    });
  
    logs.forEach(log => {
      logsTable.innerHTML += `
        <tr>
          <td>${log.logId}</td>
          <td>${log.message}</td>
          <td>${log.date}</td>
        </tr>
      `;
    });
  
    // API Cevap Süreleri ve Hata Oranı - Grafik için temel örnek
    const ctx = document.querySelector("#apiMetricsGraph");
  
    // Grafiği çizmek için basit bir örnek
    ctx.style.background = `linear-gradient(to top, rgba(0, 123, 255, 0.3) 50%, rgba(255, 0, 0, 0.3) 100%)`;
  
    // Bu kısımda bir grafik kütüphanesi (örneğin Chart.js) kullanılarak daha profesyonel bir grafik eklenebilir.
  });
  