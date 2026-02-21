import styles from "../LoginPage/LoginPage.module.scss";
import {useNavigate} from "react-router-dom";
import {Eye, EyeOff, Lock, Mail, Sparkles, User} from "lucide-react";
import {useState} from "react";
import axios from "axios";
import toast from "react-hot-toast";


const RegisterPage = () => {
    const navigate = useNavigate();
    const [showPassword, setShowPassword] = useState(false);

    const [firstName, setFirstName] = useState("");
    const [lastName, setLastName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const autoLogin = async () => {
        const response = await axios.post("http://localhost:8001/token/", {
            username: email,
            password: password,
        }, {
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
        })
        if(response.data) {
            if (response.data.access_token.length > 0) {
                localStorage.setItem("access_token", response.data.access_token);
                localStorage.setItem("user_email", email);
                navigate("/")
            }
        }
    }

    const createAccount = async () => {
        const response = await axios.post("http://localhost:8001/register/", {
            first_name: firstName,
            last_name: lastName,
            email: email,
            password: password,
        });

        if(response.data) {
            toast.success("Successfully registered!");
            await autoLogin();
        }
    }

    return (
        <div className={styles.wrapper}>
            <div className={styles.welcomeSection}>
                <div className={styles.logo}>
                    <Sparkles size={40} color="white"/>
                </div>
                <p className={styles.greet}>Create Account</p>
                <p className={styles.text}>Start finding your perfect career match</p>
            </div>
            <div className={styles.form}>
                <div className={styles.inputContainer}>
                    <label htmlFor="name">First Name</label>
                    <div className={styles.inputWrapper}>
                        <User size={20}/>
                        <input type="text"
                               placeholder="Enter your first name"
                               className={styles.input}
                               value={firstName}
                               onChange={(e) => setFirstName(e.target.value)} />
                    </div>
                </div>
                <div className={styles.inputContainer}>
                    <label htmlFor="name">Last Name</label>
                    <div className={styles.inputWrapper}>
                        <User size={20}/>
                        <input type="text"
                               placeholder="Enter your last name"
                               className={styles.input}
                               value={lastName}
                               onChange={(e) => setLastName(e.target.value)} />
                    </div>
                </div>
                <div className={styles.inputContainer}>
                    <label htmlFor="email">Email Address</label>
                    <div className={styles.inputWrapper}>
                        <Mail size={20}/>
                        <input type="text"
                               placeholder="Enter your email"
                               className={styles.input}
                               value={email}
                               onChange={(e) => setEmail(e.target.value)} />
                    </div>
                </div>
                <div className={styles.inputContainer}>
                    <label>Password</label>

                    <div className={styles.inputWrapper}>
                        <Lock size={20}/>

                        <input
                            type={showPassword ? "text" : "password"}
                            placeholder="Enter your password"
                            className={styles.input}
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />

                        {showPassword ? (
                            <EyeOff
                                size={20}
                                onClick={() => setShowPassword(false)}
                                className={styles.eyeIcon}
                            />
                        ) : (
                            <Eye
                                size={20}
                                onClick={() => setShowPassword(true)}
                                className={styles.eyeIcon}
                            />
                        )}
                    </div>
                </div>
                <button onClick={createAccount} className={styles.signInBtn}>Create Account</button>
            </div>
            <div className={styles.switchPages}>
                <span className={styles.question}>Already have an account?</span>
                <button className={styles.switchBtn} onClick={() => navigate("/login")}>Sign In</button>
            </div>
        </div>
    );
};

export default RegisterPage;