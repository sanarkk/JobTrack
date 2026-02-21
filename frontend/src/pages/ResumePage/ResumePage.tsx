import { useEffect, useRef, useState } from "react";
import axios from "axios";
import styles from "./ResumePage.module.scss";
import { Repeat2 } from "lucide-react";

interface Experience {
    company: string;
    start_date: string;
    end_date: string;
    designation: string;
    job_description: string;
}

interface ResumeResponse {
    profile_name: string;
    email: string;
    mobile_number: string;
    designation: string;
    total_experience: string;
    skills: string[];
    ai_summary: string;
    ai_strengths: string[];
    experiences: Experience[];
}

const ResumePage = () => {
    const inputRef = useRef<HTMLInputElement>(null);
    const [file, setFile] = useState<File | null>(null);
    const [resumeData, setResumeData] = useState<ResumeResponse | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchResume = async () => {
            try {
                const res = await axios.get(
                    "http://0.0.0.0:8001/my_resume/",
                    {
                        headers: {
                            Authorization: `Bearer ${
                                localStorage.getItem("access_token") || ""
                            }`,
                        },
                    }
                );

                setResumeData(res.data);
            } catch (error) {
                console.error("Failed to fetch resume:", error);
            } finally {
                setLoading(false);
            }
        };

        fetchResume();
    }, []);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const selected = e.target.files?.[0];
        if (!selected) return;
        setFile(selected);
        console.log("Selected file:", selected);
    };

    if (loading) {
        return <div className={styles.wrapper}>Loading resume...</div>;
    }

    if (!resumeData) {
        return (
            <div className={styles.wrapper}>
                Failed to load resume data.
            </div>
        );
    }

    return (
        <div className={styles.wrapper}>
            <div className={styles.info}>
                <div>
                    <p className={styles.title}>{resumeData.profile_name}</p>
                    <p className={styles.subTitle}>
                        {resumeData.designation || "No designation specified"}
                    </p>
                    <p className={styles.contact}>
                        {resumeData.mobile_number}
                    </p>
                </div>

                <button
                    className={styles.replaceBtn}
                    onClick={() => inputRef.current?.click()}
                >
                    <Repeat2 size={20} />
                    Replace Resume
                </button>
            </div>

            {resumeData.ai_summary && (
                <div className={`${styles.container}`}>
                    <p className={styles.sectionTitle}>Professional Summary</p>
                    <p className={styles.summaryText}>
                        {resumeData.ai_summary}
                    </p>
                </div>
            )}

            <div className={`${styles.skillsContainer} ${styles.container}`}>
                <div className={styles.information}>
                    <p className={styles.sectionTitle}>Skills</p>
                    <p className={styles.subTitle}>
                        Your technical and professional skills
                    </p>
                </div>

                <div className={styles.skillCards}>
                    {resumeData.skills.map((skill, index) => (
                        <div key={index} className={styles.skill}>
                            <p>{skill}</p>
                        </div>
                    ))}
                </div>
            </div>

            <div className={`${styles.experience} ${styles.container}`}>
                <div className={styles.information}>
                    <p className={styles.sectionTitle}>Experience</p>
                    <p className={styles.subTitle}>
                        Your work history and achievements
                    </p>
                </div>

                <div className={styles.experiences}>
                    {resumeData.experiences.map((exp, index) => (
                        <div key={index} className={styles.experienceItem}>
                            <p className={styles.title}>{exp.designation}</p>

                            <div className={styles.location}>
                                <p>{exp.company}</p>
                                <p>•</p>
                                <p>
                                    {exp.start_date}
                                    {exp.end_date && ` - ${exp.end_date}`}
                                </p>
                            </div>

                            <p className={styles.description}>
                                {exp.job_description}
                            </p>
                        </div>
                    ))}
                </div>
            </div>

            <input
                ref={inputRef}
                type="file"
                hidden
                accept=".pdf,.doc,.docx"
                onChange={handleChange}
            />
        </div>
    );
};

export default ResumePage;
