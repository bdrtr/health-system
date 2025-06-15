// Randevu formunun submit olayı
document.getElementById("appointmentForm").addEventListener("submit", function (e) {
    e.preventDefault();
  
    const form = e.target;
    const doctor = form.doctor.value;
    const date = form.date.value;
    const time = form.time.value;
  
    // Yeni randevu eklemek için form verilerini alıyoruz
    const newAppointment = {
      doctor,
      date,
      time,
      status: "Beklemede", // Başlangıçta "Beklemede" olarak ayarlanır
    };
  
    // Randevu bilgilerini ekliyoruz (şu an sadece ekranda gösteriliyor)
    addAppointmentToList(newAppointment);
  });
  
  // Mevcut randevuları listeleme
  function addAppointmentToList(appointment) {
    const appointmentsList = document.getElementById("appointmentsList");
  
    // Yeni randevu için HTML içeriği oluştur
    const appointmentDiv = document.createElement("div");
    appointmentDiv.classList.add("appointment");
  
    appointmentDiv.innerHTML = `
      <p><strong>Doktor:</strong> ${appointment.doctor}</p>
      <p><strong>Tarih:</strong> ${appointment.date}</p>
      <p><strong>Saat:</strong> ${appointment.time}</p>
      <p><strong>Durum:</strong> ${appointment.status}</p>
    `;
  
    // Yeni randevuyu listeye ekle
    appointmentsList.appendChild(appointmentDiv);
  }
  