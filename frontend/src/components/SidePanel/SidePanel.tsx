import styles from "./SidePanel.module.scss";
import {
    LayoutDashboard,
    FileText,
    MessageCircleMore,
    LogOut,
    FileHeart,
    // Database
} from "lucide-react";
import {NavLink, useNavigate} from "react-router-dom";
import {useEffect, useState} from "react";
import axios from "axios";

interface userData {
    email: string;
    first_name: string;
    id: string
    last_name: string;
    password: string;
}

const SidePanel = () => {

    const navigate = useNavigate();
    const [userData, setUserData] = useState<userData | null>(null);

    const initials = `${userData?.first_name?.[0] ?? ""}${userData?.last_name?.[0] ?? ""}`.toUpperCase()


    const navItems = [
        { label: "Dashboard", icon: LayoutDashboard, path: "/dashboard" },
        { label: "My Resume", icon: FileText, path: "/resume" },
        { label: "My Saved", icon: FileHeart, path: "/saved" },
        { label: "AI Assistant", icon: MessageCircleMore, path: "/ai-assistant" },
    ];

    const handleLogOut = () => {
        const isConfirmed = confirm("Are you sure that you want to log out?");
        if (isConfirmed) {
            localStorage.removeItem("access_token");
            navigate("/login");
        }
    }

    useEffect(() => {
        const fetchUser = async () => {
            const token = localStorage.getItem("access_token")
            if (!token) return

            try {
                const res = await axios.post(
                    "http://localhost:8001/me/",
                    {},
                    {
                        headers: {
                            Authorization: `Bearer ${token}`,
                        },
                    }
                )
                console.log(res.data)
                setUserData(res.data)
            } catch (err) {
                console.error("Failed to fetch user")
            }
        }
        fetchUser()
    }, [])


    return (
        <div className={styles.wrapper}>
            <div className={styles.header}>
                <div className={styles.userLogo}>
                    <h2>{initials}</h2>
                </div>
                <div className={styles.credentials}>
                    <p className={styles.name}>
                        {userData?.first_name} {userData?.last_name}
                    </p>
                    <p className={styles.email}>{userData?.email}</p>
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
                <button onClick={handleLogOut} className={styles.logoutBtn}>
                    <LogOut size={20}/>
                    <span>Sign Out</span>
                </button>
            </div>
        </div>
    );
};

export default SidePanel;
