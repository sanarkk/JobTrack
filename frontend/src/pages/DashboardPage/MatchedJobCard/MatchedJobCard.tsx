import styles from "./MatchedJobCard.module.scss";
import {MapPin} from "lucide-react"

interface MatchedJob {
    title: string,
    shortDescription: string,
    companyName: string,
    location: string,
    onSite: boolean,
    skills: string[],
    salary: string,
    matchRate: number,
}

interface MatchedJobCardProps {
    job: MatchedJob;
    index: number;
    onViewDetails?: () => void;
}

const MatchedJobCard = ({job, index, onViewDetails}: MatchedJobCardProps) => {
    return (
        <div className={styles.job} key={index}>
            <div className={styles.mainInfo}>
                <div className={styles.info}>
                    <div className={styles.titleInfo}>
                        <span className={styles.title}>{job.title}</span>
                        <span className={styles.matchRate}>{job.matchRate}% match</span>
                    </div>
                    <div className={styles.companyInfo}>
                        <span className={styles.companyName}>{job.companyName}</span>
                        <span className={styles.location}><MapPin size={14}/>{job.location}</span>
                        <span className={styles.onSite}>{job.onSite ? "On site" : "Remote"}</span>
                    </div>
                </div>
                <div className={styles.salarySection}>
                    <p className={styles.salaryText}>Salary range</p>
                    <p className={styles.salary}>{job.salary}</p>
                </div>
            </div>
            <div className={styles.body}>
                <p className={styles.description}>{job.shortDescription}</p>
                <div className={styles.skills}>
                    {job.skills.map((skill, index) => (
                        <div className={styles.skill} key={index}>
                            {skill}
                        </div>
                    ))}
                </div>
            </div>
            <div className={styles.btns}>
                <button onClick={onViewDetails} className={styles.detailsBtn}>View details</button>
                <button className={styles.saveBtn}>Save</button>
            </div>
        </div>
    );
};

export default MatchedJobCard;