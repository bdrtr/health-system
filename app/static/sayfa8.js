// "Teşhisi Kaydet" butonuna tıklanma olayı
document.getElementById("saveDiagnosisButton").addEventListener("click", function () {
    const diagnosis = document.getElementById("manualDiagnosis").value;
    
    if (diagnosis) {
      alert("Teşhis başarıyla kaydedildi.");
      // Burada API'ye gönderim yapılabilir
    } else {
      alert("Lütfen manuel teşhisi girin.");
    }
  });
  
  // "Tedavi Planı Ekle" butonuna tıklanma olayı
  document.getElementById("addTreatmentButton").addEventListener("click", function () {
    alert("Tedavi planı eklenmeye yönlendiriliyorsunuz.");
    // Burada tedavi planı ekleme işlemi yapılabilir
  });
  