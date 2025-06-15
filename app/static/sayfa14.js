// Silinen kullanıcılar verisi
const deletedUsers = [
    { name: 'Ahmet Yılmaz', role: 'Hasta', deletedDate: '2025-04-30' },
    { name: 'Ayşe Demir', role: 'Doktor', deletedDate: '2025-04-28' },
  ];
  
  // Silinen kullanıcıları listele
  function displayDeletedUsers() {
    const tableBody = document.querySelector('#deletedUserTable tbody');
    tableBody.innerHTML = ''; // Tabloyu temizle
    deletedUsers.forEach(user => {
      const row = document.createElement('tr');
      
      row.innerHTML = `
        <td>${user.name}</td>
        <td>${user.role}</td>
        <td>${user.deletedDate}</td>
      `;
      
      tableBody.appendChild(row);
    });
  }
  
  // Sayfa yüklendiğinde silinen kullanıcıları listele
  document.addEventListener('DOMContentLoaded', displayDeletedUsers);
  