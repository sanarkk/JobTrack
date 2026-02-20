import styles from "./LoginPage.module.scss";
import { Sparkles, Mail, Lock, Eye, EyeOff } from 'lucide-react';

import {useNavigate} from "react-router-dom";
import {useState} from "react";
import axios from "axios";
import toast from "react-hot-toast";

const LoginPage = () => {
    const navigate = useNavigate();
    const [showPassword, setShowPassword] = useState(false);
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const loginUser = async () => {
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
                toast.success("Successfully logged in!");
            }
        }
    }

    return (
        <div className={styles.wrapper}>
            <div className={styles.welcomeSection}>
                <div className={styles.logo}>
                    <Sparkles size={40} color="white"/>
                </div>
                <p className={styles.greet}>Welcome back</p>
                <p className={styles.text}>Sign in to continue your job search journey</p>
            </div>
            <div className={styles.form}>
                <div className={styles.inputContainer}>
                    <label htmlFor="email">Email Address</label>
                    <div className={styles.inputWrapper}>
                        <Mail size={20} />
                        <input type="text"
                               placeholder="Enter your email"
                               className={styles.input}
                               value={email}
                               onChange={(e) => setEmail(e.target.value)}
                        />
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
                <button onClick={loginUser} className={styles.signInBtn}>Sign in</button>
            </div>
            <div className={styles.switchPages}>
                <span className={styles.question}>Don't have an account?</span>
                <button className={styles.switchBtn} onClick={() => navigate("/register")}>Create an account</button>
            </div>
        </div>
    );
};

export default LoginPage;