import { useEffect, useState } from "react";
import NoResumePage from "./NoResumePage/NoResumePage";
import styles from "./DashboardPage.module.scss";
import MatchedJobCard from "./MatchedJobCard/MatchedJobCard";
import MatchedJobPopup from "./MatchedJobPopup/MatchedJobPopup";
import axios from "axios";

interface MatchedJob {
    id: string;
    job_title: string;
    job_category: string;
    seniority_level: string;
    requirements_summary: string;
    technical_tools: string[];
    formatted_workplace_location: string;
    province: string;
    commitment: string;
    workplace_type: string;
    yearly_min_compensation: number;
    yearly_max_compensation: number;
    company_name: string;
    apply_url: string;
    source_file: string;
    hash: string;
}

const DashboardPage = () => {
    const hasResume = true;

    const [selectedJob, setSelectedJob] = useState<MatchedJob | null>(null);
    const [matchedJobs, setMatchedJobs] = useState<MatchedJob[]>([]);
    const [savedJobIds, setSavedJobIds] = useState<string[]>([]);

    useEffect(() => {
        const fetchJobs = async () => {
            try {
                const res = await axios.get("http://localhost:8001/all/");
                setMatchedJobs(res.data);
            } catch (error) {
                console.log(error);
            }
        };

        fetchJobs();
    }, []);

    useEffect(() => {
        const fetchSavedJobs = async () => {
            try {
                const res = await axios.get(
                    "http://localhost:8001/get_all_saved_jobs",
                    {
                        headers: {
                            Authorization: `Bearer ${
                                localStorage.getItem("access_token") || ""
                            }`,
                        },
                    }
                );

                const ids = [...new Set(res.data.map((job: any) => job.job_id))];

                // @ts-ignore
                setSavedJobIds(ids);
            } catch (error) {
                console.log(error);
            }
        };

        fetchSavedJobs();
    }, []);


    const handleSaveSuccess = (jobId: string) => {
        setSavedJobIds((prev) => [...prev, jobId]);
    };

    return (
        <div className={styles.wrapper}>
            {!hasResume ? (
                <NoResumePage />
            ) : (
                <div className={styles.content}>
                    <div className={styles.info}>
                        <p className={styles.title}>Your Job Matches</p>
                        <p className={styles.subTitle}>
                            Personalized recommendations based on your resume and preferences
                        </p>
                    </div>

                    <div className={styles.matchedJobs}>
                        {matchedJobs.map((job, index) => (
                            <MatchedJobCard
                                key={job.id}
                                job={job}
                                index={index}
                                isSaved={savedJobIds.includes(job.id)}
                                variant="dashboard"
                                onSaveSuccess={handleSaveSuccess}
                                onViewDetails={() => setSelectedJob(job)}
                            />
                        ))}
                    </div>
                </div>
            )}

            {selectedJob && (
                <MatchedJobPopup
                    job={selectedJob}
                    variant="dashboard"
                    isSaved={savedJobIds.includes(selectedJob.id)}
                    onSave={() => handleSaveSuccess(selectedJob.id)}
                    onClose={() => setSelectedJob(null)}
                />
            )}
        </div>
    );
};

export default DashboardPage;
