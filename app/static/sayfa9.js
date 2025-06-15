document.getElementById('treatmentForm').addEventListener('submit', function(event) {
    event.preventDefault();
  
    // Kullanıcıdan gelen verileri al
    const patientName = document.getElementById('patientName').value;
    const fractureType = document.getElementById('fractureType').value;
    const treatmentPlan = document.getElementById('treatmentPlan').value;
  
    // Verileri bir objeye kaydet
    const treatmentData = {
      patientName: patientName,
      fractureType: fractureType,
      treatmentPlan: treatmentPlan
    };
  
    // Veriyi localStorage'a kaydet (bunu sunucuya kaydedebilirsin)
    localStorage.setItem('treatmentPlanData', JSON.stringify(treatmentData));
  
    // Başarı mesajı göster
    const successMsg = document.getElementById('successMsg');
    successMsg.textContent = 'Tedavi Planı başarıyla kaydedildi!';
  
    // Formu sıfırla
    document.getElementById('treatmentForm').reset();
  });
  