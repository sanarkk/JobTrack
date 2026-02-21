import styles from './NoResumePage.module.scss';
import { Upload } from "lucide-react";
import axios from "axios";
import { useState } from "react";

interface StatInfoItem {
    metric: string;
    description: string;
}

const NoResumePage = () => {
    const [uploading, setUploading] = useState(false);

    const statsInfo: StatInfoItem[] = [
        { metric: "AI-Powered", description: "Smart Matching" },
        { metric: "1000+", description: "Active Jobs" },
        { metric: "95%", description: "Match Accuracy" },
    ];

    const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (!file) return;

        try {
            setUploading(true);

            const formData = new FormData();
            formData.append("file", file);

            await axios.post(
                "http://0.0.0.0:8001/upload_resume",
                formData,
                {
                    headers: {
                        Authorization: `Bearer ${
                            localStorage.getItem("access_token") || ""
                        }`,
                        "Content-Type": "multipart/form-data",
                    },
                }
            );

            window.location.reload();

        } catch (error) {
            console.error("Resume upload failed:", error);
        } finally {
            setUploading(false);
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
                    Upload your resume to unlock AI-powered job recommendations
                    tailored specifically to your skills and experience.
                </p>

                <label className={styles.uploadLogoBtn}>
                    <Upload size={24}/>
                    {uploading ? "Uploading..." : "Upload Your Resume"}

                    <input
                        type="file"
                        hidden
                        accept=".pdf,.doc,.docx"
                        onChange={handleFileChange}
                        disabled={uploading}
                    />
                </label>
            </div>

            <div className={styles.stats}>
                {statsInfo.map((stat) => (
                    <div key={stat.metric} className={styles.stat}>
                        <p className={styles.metric}>{stat.metric}</p>
                        <p className={styles.description}>{stat.description}</p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default NoResumePage;
