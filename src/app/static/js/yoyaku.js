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

const btn__ = document.getElementById('add-transfer')
let transferCount = 0;
btn__.addEventListener('click', function () {
    const transferContainer = document.getElementById('transfer-container');
    if (transferCount < 2) {
        const newTransferDiv = document.createElement('div');
        newTransferDiv.classList.add('field-group');

        const newTransferLabel = document.createElement('label');
        newTransferLabel.setAttribute('for', 'transfer' + (transferCount + 1));
        newTransferLabel.textContent = '乗り換え' + (transferCount + 1) + '：';

        const newTransferInput = document.createElement('input');
        newTransferInput.setAttribute('type', 'text');
        newTransferInput.setAttribute('id', 'transfer' + (transferCount + 1));

        const removeButton = document.createElement('button');
        removeButton.textContent = '×';
        removeButton.classList.add('remove-transfer');
        removeButton.addEventListener('click', () => {
            transferContainer.removeChild(transferContainer.lastChild);
            if (btn__.style.display == 'none') {
                btn__.style.display = 'block';
            }
            transferCount--;
        });

        newTransferDiv.appendChild(newTransferLabel);
        newTransferDiv.appendChild(newTransferInput);
        newTransferDiv.appendChild(removeButton);
        transferContainer.append(newTransferDiv);
    }

    if (transferCount + 1 >= 2) {
        this.style.display = 'none';
    }
    transferCount++;
});