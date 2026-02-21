import { useState } from "react";
import NoResumePage from "./NoResumePage/NoResumePage";
import styles from "./DashboardPage.module.scss";
import MatchedJobCard from "./MatchedJobCard/MatchedJobCard.tsx";
import MatchedJobPopup from "./MatchedJobPopup/MatchedJobPopup.tsx";

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

const DashboardPage = () => {
    const [hasResume, setHasResume] = useState(true);
    const [selectedJob, setSelectedJob] = useState<MatchedJob | null>(null);


    const matchedJobs = [
        {
            title: "Senior Frontend Engineer",
            shortDescription: "Build scalable web applications with modern frameworks",
            companyName: "TechCorp",
            location: "San Francisco, CA, USA",
            onSite: false,
            skills: ["React", "TypeScript", "SCSS", "Axios"],
            salary: "$140k - $180k",
            matchRate: 95
        },
        {
            title: "Senior Frontend Engineer",
            shortDescription: "Build scalable web applications with modern frameworks",
            companyName: "TechCorp",
            location: "San Francisco, CA, USA",
            onSite: true,
            skills: ["React", "TypeScript", "SCSS", "Axios"],
            salary: "$140k - $180k",
            matchRate: 90
        },
        {
            title: "Senior Frontend Engineer",
            shortDescription: "Build scalable web applications with modern frameworks",
            companyName: "TechCorp",
            location: "San Francisco, CA, USA",
            onSite: false,
            skills: ["React", "TypeScript", "SCSS", "Axios"],
            salary: "$140k - $180k",
            matchRate: 85
        },
        {
            title: "Senior Frontend Engineer",
            shortDescription: "Build scalable web applications with modern frameworks",
            companyName: "TechCorp",
            location: "San Francisco, CA, USA",
            onSite: true,
            skills: ["React", "TypeScript", "SCSS", "Axios"],
            salary: "$140k - $180k",
            matchRate: 75
        },
        {
            title: "Senior Frontend Engineer",
            shortDescription: "Build scalable web applications with modern frameworks",
            companyName: "TechCorp",
            location: "San Francisco, CA, USA",
            onSite: false,
            skills: ["React", "TypeScript", "SCSS", "Axios"],
            salary: "$140k - $180k",
            matchRate: 95
        },
        {
            title: "Senior Frontend Engineer",
            shortDescription: "Build scalable web applications with modern frameworks",
            companyName: "TechCorp",
            location: "San Francisco, CA, USA",
            onSite: false,
            skills: ["React", "TypeScript", "SCSS", "Axios"],
            salary: "$140k - $180k",
            matchRate: 95
        },
        {
            title: "Senior Frontend Engineer",
            shortDescription: "Build scalable web applications with modern frameworks",
            companyName: "TechCorp",
            location: "San Francisco, CA, USA",
            onSite: false,
            skills: ["React", "TypeScript", "SCSS", "Axios"],
            salary: "$140k - $180k",
            matchRate: 95
        },

    ]

    return (
        <div className={styles.wrapper}>
            {!hasResume ? (
                <NoResumePage onConfirm={() => setHasResume(true)} />
            ) : (
                <div className={styles.content}>
                    <div className={styles.info}>
                        <p className={styles.title}>Your Job Matches</p>
                        <p className={styles.subTitle}>Personalized recommendations based on your resume and
                            preferences</p>
                    </div>
                    <div className={styles.matchedJobs}>
                        {matchedJobs.map((job, index) => (
                            <MatchedJobCard job={job} index={index} onViewDetails={() => setSelectedJob(job)}/>
                        ))}
                    </div>
                </div>
            )}
            {selectedJob && (
                <MatchedJobPopup job={selectedJob} onClose={() => setSelectedJob(null)} />
            )}
        </div>
    );
};

export default DashboardPage;
