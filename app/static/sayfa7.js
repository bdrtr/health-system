// Hastaların bilgilerini saklamak
const patientsData = {
    "Ahmet Yılmaz": {
        age: 45,
        diagnosis: "Ağır bronşit",
        lastXRayDate: "2025-04-20",
        xrayLink: "xray1.jpg"
    },
    "Ayşe Demir": {
        age: 30,
        diagnosis: "Baş ağrısı ve migren",
        lastXRayDate: "2025-03-15",
        xrayLink: "xray2.jpg"
    }
};

// Modal'ı açmak için fonksiyon
function showPatientDetails(name) {
    const patient = patientsData[name];

    if (patient) {
        // Modal içeriğini güncelle
        document.getElementById("modalTitle").innerText = `${name} - Detaylar`;
        document.getElementById("patientAge").innerText = patient.age;
        document.getElementById("patientDiagnosis").innerText = patient.diagnosis;
        document.getElementById("patientXRayDate").innerText = patient.lastXRayDate;
        document.getElementById("modalXRayImage").src = patient.xrayLink;

        // Modal'ı göster
        document.getElementById("patientModal").style.display = "block";
    }
}

// Modal'ı kapatmak için fonksiyon
function closeModal() {
    document.getElementById("patientModal").style.display = "none";
}
