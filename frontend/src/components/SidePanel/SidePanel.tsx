import styles from "./SidePanel.module.scss";
import {
    LayoutDashboard,
    FileText,
    MessageCircleMore,
    Upload,
    LogOut,
    FileHeart,
} from "lucide-react";
import {NavLink, useNavigate} from "react-router-dom";

const SidePanel = () => {

    const navigate = useNavigate();

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
            //TODO send resume to backend
        }
    };

    const handleLogOut = () => {
        const isConfirmed = confirm("Are you sure that you want to log out?");
        if (isConfirmed) {
            localStorage.removeItem("access_token");
            localStorage.removeItem("user_email");
            navigate("/login");
        }
    }

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
                <button onClick={handleLogOut} className={styles.logoutBtn}>
                    <LogOut size={20}/>
                    <span>Sign Out</span>
                </button>
            </div>
        </div>
    );
};

export default SidePanel;
