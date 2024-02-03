//dashboard.js

var currentRoomNumber = null;

function showCheckInForm(roomNumber) {
    // Define a ação do formulário com o número do quarto
    var form = document.querySelector('#checkInFormSection form');
    form.action = '/create_booking/' + roomNumber + '/';

    // Exibe o formulário
    document.getElementById('checkInFormSection').style.display = 'block';
}

function closeCheckInForm() {
    document.getElementById('checkInFormSection').style.display = 'none';
}

function showOccupiedRoomOptions(roomNumber) {
    currentRoomNumber = roomNumber;
    document.getElementById('OccupiedRoomOptions').style.display='block';
    // Código para mostrar os botões de opções para um quarto ocupado.
    // Por exemplo, você pode ter um modal ou um elemento na página que é atualizado e exibido aqui.
}

function closeOccupiedRoomOptions(roomNumber){
    document.getElementById('OccupiedRoomOptions').style.display = 'none';
}

function expandRoomData() {
    if (currentRoomNumber) {
        // Aqui você pode redirecionar o usuário para uma nova página com detalhes
        // Ou pode fazer uma requisição AJAX para buscar os dados e exibi-los
        window.location.href = '/room/' + currentRoomNumber + '/details/';
    }
}