import styles from "./SidePanel.module.scss";
import {
    LayoutDashboard,
    FileText,
    MessageCircleMore,
    Upload,
    LogOut,
    FileHeart,
} from "lucide-react";
import { NavLink } from "react-router-dom";

const SidePanel = () => {

    const navItems = [
        { label: "Dashboard", icon: LayoutDashboard, path: "/dashboard" },
        { label: "My Resume", icon: FileText, path: "/resume" },
        { label: "My Saved", icon: FileHeart, path: "/saved" },
        { label: "AI Assistant", icon: MessageCircleMore, path: "/ai-assistant" },
    ];

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            console.log("Selected file:", file);
            //TODO send file to backend
        }
    };

    return (
        <div className={styles.wrapper}>
            <div className={styles.header}>
                <div className={styles.userLogo}>
                    <h2>YD</h2>
                </div>
                <div className={styles.credentials}>
                    <p className={styles.name}>Yaroslav Dimbrovskyi</p>
                    <p className={styles.email}>yarikdimbrovsky@gmail.com</p>
                </div>
            </div>

            <div className={styles.navBtns}>
                {navItems.map(({ label, icon: Icon, path }) => (
                    <NavLink
                        key={path}
                        to={path}
                        className={({ isActive }) =>
                            `${styles.btn} ${isActive ? styles.active : ""}`
                        }
                    >
                        <Icon size={20} />
                        <p>{label}</p>
                    </NavLink>
                ))}
            </div>

            <div className={styles.footer}>
                <label className={styles.uploadLogoBtn}>
                    <Upload size={20}/>
                    <span>Upload Resume</span>
                    <input
                        type="file"
                        hidden
                        accept=".pdf,.doc,.docx"
                        onChange={handleFileChange}
                    />
                </label>
                <NavLink to="/login" className={styles.logoutBtn}>
                    <LogOut size={20}/>
                    <span>Sign Out</span>
                </NavLink>
            </div>
        </div>
    );
};

export default SidePanel;
