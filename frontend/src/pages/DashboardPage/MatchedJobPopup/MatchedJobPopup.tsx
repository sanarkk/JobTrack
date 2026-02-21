import styles from "./MatchedJobPopup.module.scss";
import { ArrowLeft, MapPin, TrendingUp, Briefcase,} from "lucide-react";

interface MatchedJobPopupProps {
    job: {
        title: string,
        shortDescription: string,
        companyName: string,
        location: string,
        onSite: boolean,
        skills: string[],
        salary: string,
        matchRate: number,
    };
    onClose: () => void;
}

const MatchedJobPopup = ({ job, onClose }: MatchedJobPopupProps) => {

    return (
        <div className={styles.overlay}>
            <div className={styles.container}>
                <button className={styles.backBtn} onClick={onClose}>
                    <ArrowLeft size={20}/>
                    <span>Back to Job Matches</span>
                </button>
                <div className={styles.job} key={job.title}>
                    <div className={styles.mainInfo}>
                        <div className={styles.info}>
                            <div className={styles.titleInfo}>
                                <span className={styles.title}>{job.title}</span>
                            </div>
                            <div className={styles.companyInfo}>
                                <span className={styles.companyName}>{job.companyName}</span>
                                <span className={styles.location}><MapPin size={14}/>{job.location}</span>
                                <span className={styles.onSite}>{job.onSite ? "On site" : "Remote"}</span>
                            </div>
                            <div style={{display: "flex", gap: 12}}>
                                <span className={styles.matchRate}><TrendingUp size={20}/>{job.matchRate}% match</span>
                                <span className={styles.workType}><Briefcase size={20}/>Full time</span>
                            </div>
                        </div>
                        <div className={styles.salarySection}>
                            <p className={styles.salaryText}>Salary range</p>
                            <p className={styles.salary}>{job.salary}</p>
                        </div>
                    </div>
                    <div className={styles.btns}>
                        <button className={styles.detailsBtn}>Apply</button>
                        <button className={styles.saveBtn}>Save</button>
                    </div>
                </div>
                <div className={styles.description}>
                    <p className={styles.title}>Description</p>
                    <p className={styles.text}>{job.shortDescription}</p>
                </div>
                <div className={styles.skillContainer}>
                <p className={styles.title}>Required Skills</p>
                    <div className={styles.skills}>
                        {job.skills.map((skill, index) => (
                            <div className={styles.skill} key={index}>
                                {skill}
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default MatchedJobPopup;
