const passwordGenerator = (len: number) => {
        
            const lower = "abcdefghijklmnopqrstuvwxyz";
            const upperChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
            const numChars = "0123456789";
            const specialChars = "!@#$%^&*()-_=+[]{}|;:,.<>?";
            let chars = lower + upperChars + numChars + specialChars;

            let pass = "";
            for (let i = 0; i < len; i++) {
                const randIdx = Math.floor(Math.random() * chars.length);
                pass += chars[randIdx];
            }

            const password_form = (document.getElementById("form-password") as HTMLInputElement);
            if (password_form) {
                password_form.value = pass    
            }

            // return pass;
    }