import styles from "../LoginPage/LoginPage.module.scss";
import {useNavigate} from "react-router-dom";
import {Eye, EyeOff, Lock, Mail, Sparkles, User} from "lucide-react";
import {useState} from "react";

const RegisterPage = () => {
    const navigate = useNavigate();
    const [showPassword, setShowPassword] = useState(false);

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
                        <input type="text" placeholder="Enter your first name" className={styles.input}/>
                    </div>
                </div>
                <div className={styles.inputContainer}>
                    <label htmlFor="name">Last Name</label>
                    <div className={styles.inputWrapper}>
                        <User size={20}/>
                        <input type="text" placeholder="Enter your last name" className={styles.input}/>
                    </div>
                </div>
                <div className={styles.inputContainer}>
                    <label htmlFor="email">Email Address</label>
                    <div className={styles.inputWrapper}>
                        <Mail size={20}/>
                        <input type="text" placeholder="Enter your email" className={styles.input}/>
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
                <button className={styles.signInBtn}>Create Account</button>
            </div>
            <div className={styles.switchPages}>
                <span className={styles.question}>Already have an account?</span>
                <button className={styles.switchBtn} onClick={() => navigate("/login")}>Sign In</button>
            </div>
        </div>
    );
};

export default RegisterPage;