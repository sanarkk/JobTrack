import { useState } from "react";
import NoResumePage from "./NoResumePage/NoResumePage";
import styles from "./DashboardPage.module.scss";

const DashboardPage = () => {
    const [hasResume, setHasResume] = useState(false);

    return (
        <div className={styles.wrapper}>
            {!hasResume ? (
                <NoResumePage onConfirm={() => setHasResume(true)} />
            ) : (
                <div>
                    <h2>Dashboard Section with Resume</h2>
                </div>
            )}
        </div>
    );
};

export default DashboardPage;
