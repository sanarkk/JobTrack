import styles from './NoResumePage.module.scss';
import { Upload } from "lucide-react";

const NoResumePage = () => {

    interface statInfoItem {
        metric: string;
        description: string;
    }

    const statsInfo: statInfoItem[] = [
        {
            metric: "AI-Powered",
            description: "Start matching"
        },
        {
            metric: "1000+",
            description: "Active Jobs"
        },
        {
            metric: "95%",
            description: "Match Accuracy"
        },
    ];

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            console.log("Selected file:", file);
            //send file to backend to change the page layout
        }
    };

    return (
        <div className={styles.wrapper}>
            <div className={styles.content}>
                <div className={styles.uploadContainer}>
                    <Upload size={40}/>
                </div>

                <p className={styles.title}>
                    Let's Find Your Perfect Job Match
                </p>

                <p className={styles.text}>
                    Upload your resume to unlock AI-powered job recommendations tailored specifically to your skills,
                    experience, and career goals. Our intelligent matching system analyzes thousands of opportunities to
                    find the best fits for you.
                </p>


                <label className={styles.uploadLogoBtn}>
                    <Upload size={24}/>
                    Upload Your Resume
                    <input
                        type="file"
                        hidden
                        accept=".pdf,.doc,.docx"
                        onChange={handleFileChange}
                    />
                </label>

            </div>

            <div className={styles.stats}>
                {statsInfo.map((stat) => (
                    <div key={stat.metric} className={styles.stat}>
                        <p className={styles.metric}>
                            {stat.metric}
                        </p>
                        <p className={styles.description}>
                            {stat.description}
                        </p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default NoResumePage;
