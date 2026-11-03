const copyButton = document.querySelector("#copy-button");
const passwordText = document.querySelector("#generated-password");
const copyMessage = document.querySelector("#copy-message");

if (copyButton && passwordText && copyMessage) {
    copyButton.addEventListener("click", async () => {
        try {
            await navigator.clipboard.writeText(passwordText.textContent);
            copyMessage.textContent = "Password copied successfully.";
        } catch (error) {
            copyMessage.textContent = "Please select and copy the password manually.";
        }
    });
}
