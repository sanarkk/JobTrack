import styles from "./ResumePage.module.scss";
import {Repeat2} from "lucide-react";
import {useRef, useState} from "react";

const ResumePage = () => {
    const inputRef = useRef<HTMLInputElement>(null);
    const [file, setFile] = useState<File | null>(null);


    const skills = ["React", "TypeScript", "SCSS", "NodeJS", "Python"];

    const experiences = [
        {
            title: "Senior Frontend Developer",
            place: "Tech Solutions INC",
            date: "2021 - Present",
            description: "Lead development of customer-facing web applications using React and TypeScript. Improved application performance by 60% and mentored 5 junior developers."
        },
        {
            title: "Senior Python Developer",
            place: "Big Tech INC",
            date: "2021 - Present",
            description: "Lead development of customer-facing web applications usingLead development of customer-facing web applications using React and TypeScript. Improved application performance by 60% and mentored 5 junior developers."
        }
    ];

    const education = [
        {
            faculty: "Bachelor of Science in Computer Science",
            place: "University of Manitoba",
            date: "2021 - Present",
        }
    ];

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const selected = e.target.files?.[0]
        if (!selected) return

        setFile(selected);
        console.log(selected)
        console.log(file)
    }

    return (
        <div className={styles.wrapper}>
            <div className={styles.info}>
                <p className={styles.title}>My Resume</p>
                <button
                    className={styles.replaceBtn}
                    onClick={() => inputRef.current?.click()}
                >
                    <Repeat2 size={20}/>
                    Replace Your Resume
                </button>
            </div>

            <div className={`${styles.skillsContainer} ${styles.container}`}>
                <div className={styles.information}>
                    <p className={styles.title}>Skills</p>
                    <p className={styles.subTitle}>Your technical and professional skills</p>
                </div>
                <div className={styles.skillCards}>
                    {skills.map((skill, index) => (
                        <div key={index} className={styles.skill}>
                            <p>{skill}</p>
                        </div>
                    ))}
                </div>
            </div>

            <div className={`${styles.experience} ${styles.container}`}>
                <div className={styles.information}>
                    <p className={styles.title}>Experience</p>
                    <p className={styles.subTitle}>Your work history and achievements</p>
                </div>
                <div className={styles.experiences}>
                    {experiences.map((experience, index) => (
                        <div key={index} className={styles.experienceItem}>
                            <p className={styles.title}>{experience.title}</p>
                            <div className={styles.location}>
                                <p>{experience.place}</p>
                                <p>•</p>
                                <p>{experience.date}</p>
                            </div>
                            <p className={styles.description}>{experience.description}</p>
                        </div>
                    ))}
                </div>
            </div>

            <div className={`${styles.education} ${styles.container}`}>
                <div className={styles.information}>
                    <p className={styles.title}>Education</p>
                    <p className={styles.subTitle}>Your academic background</p>
                </div>
                {education.map((edu, index) => (
                    <div key={index} className={styles.educationItem}>
                        <p className={styles.faculty}>{edu.faculty}</p>
                        <div className={styles.location}>
                            <p>{edu.place}</p>
                            <p>•</p>
                            <p>{edu.date}</p>
                        </div>
                    </div>
                ))}
            </div>

            <input
                ref={inputRef}
                type="file"
                hidden
                accept=".pdf"
                onChange={handleChange}
            />
        </div>
    );
};

export default ResumePage;