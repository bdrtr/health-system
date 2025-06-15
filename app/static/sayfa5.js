// Örnek röntgen raporları
const reports = [
    {
      imageUrl: 'xray1.jpg', // Bu, röntgenin görseli olacak
      diagnosis: 'Forearm Fracture',
      status: 'Tespit Edildi',
      confidence: '85%',
      doctorComment: 'Kırık bölgesine sabırlı bir iyileşme süreci gerekmektedir.',
      treatmentPlan: 'Ağrı kesiciler ve fiziksel terapi önerilmektedir.',
    },
    {
      imageUrl: 'xray2.jpg',
      diagnosis: 'Shoulder Dislocation',
      status: 'Bekliyor',
      confidence: '78%',
      doctorComment: 'Omuzda ciddi bir çıkık görünümü var.',
      treatmentPlan: 'Cerrahi müdahale gerekebilir.',
    },
    {
      imageUrl: 'xray3.jpg',
      diagnosis: 'Leg Fracture',
      status: 'Reddedildi',
      confidence: '55%',
      doctorComment: 'Bu, bir kırık değil, kas gerilmesidir.',
      treatmentPlan: 'Dinlenme ve soğuk kompres önerilmektedir.',
    },
  ];
  
  document.addEventListener('DOMContentLoaded', function () {
    const reportsList = document.getElementById('reportsList');
  
    // Raporları listele
    reports.forEach((report) => {
      const reportCard = document.createElement('div');
      reportCard.classList.add('report-card');
  
      reportCard.innerHTML = `
        <div class="report-header">
          <span>Durum: <span class="status">${report.status}</span></span>
          <span>Güven Skoru: ${report.confidence}</span>
        </div>
        <div class="report-body">
          <div class="details">
            <span>Teşhis: </span><strong>${report.diagnosis}</strong>
          </div>
          <div class="details">
            <span>Doktor Yorumu: </span><em>${report.doctorComment}</em>
          </div>
          <div class="details">
            <span>Tedavi Planı: </span><em>${report.treatmentPlan}</em>
          </div>
          <div class="details">
            <a href="#">Röntgeni Görüntüle</a>
          </div>
          <img src="${report.imageUrl}" alt="Röntgen Görseli" class="image">
        </div>
      `;
  
      reportsList.appendChild(reportCard);
    });
  });
  