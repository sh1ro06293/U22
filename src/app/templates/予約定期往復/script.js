document.querySelectorAll('.selectable').forEach(button => {
    button.addEventListener('click', function() {
        const group = button.dataset.group;
        if (group) {
            // 同じグループの他のボタンをすべて未選択にする
            document.querySelectorAll(`.selectable[data-group="${group}"]`).forEach(b => b.classList.remove('selected'));
        }
        // 自分自身の選択状態を切り替える
        button.classList.toggle('selected');
    });
});

function addTransferHandler(containerId, buttonId) {
    document.getElementById(buttonId).addEventListener('click', function() {
        const transferContainer = document.getElementById(containerId);
        const transferCount = transferContainer.children.length;

        if (transferCount < 2) {
            const newTransferDiv = document.createElement('div');
            newTransferDiv.classList.add('field-group');

            const newTransferLabel = document.createElement('label');
            newTransferLabel.setAttribute('for', containerId + '-transfer' + (transferCount + 1));
            newTransferLabel.textContent = '乗り換え' + (transferCount + 1) + '：';

            const newTransferInput = document.createElement('input');
            newTransferInput.setAttribute('type', 'text');
            newTransferInput.setAttribute('id', containerId + '-transfer' + (transferCount + 1));

            const removeButton = document.createElement('button');
            removeButton.textContent = '×';
            removeButton.classList.add('remove-transfer');
            removeButton.addEventListener('click', function() {
                transferContainer.removeChild(newTransferDiv);
                document.getElementById(buttonId).style.display = 'block';
            });

            newTransferDiv.appendChild(newTransferLabel);
            newTransferDiv.appendChild(newTransferInput);
            newTransferDiv.appendChild(removeButton);
            transferContainer.appendChild(newTransferDiv);
        }

        if (transferCount + 1 >= 2) {
            this.style.display = 'none';
        }
    });
}

addTransferHandler('transfer-container1', 'add-transfer1');
addTransferHandler('transfer-container2', 'add-transfer2');

document.addEventListener("DOMContentLoaded", function() {
    const everydayButton = document.getElementById('everyday');
    const weekButton = document.getElementById('week');

    function toggleButton(selectedButton, otherButton) {
        selectedButton.classList.add('selected');
        otherButton.classList.remove('selected');
    }

    everydayButton.addEventListener('click', function() {
        toggleButton(everydayButton, weekButton);
    });

    weekButton.addEventListener('click', function() {
        toggleButton(weekButton, everydayButton);
    });
});
