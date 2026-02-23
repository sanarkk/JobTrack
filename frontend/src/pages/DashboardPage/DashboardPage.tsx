import { useEffect, useState } from "react";
import NoResumePage from "./NoResumePage/NoResumePage";
import styles from "./DashboardPage.module.scss";
import MatchedJobCard from "./MatchedJobCard/MatchedJobCard";
import MatchedJobPopup from "./MatchedJobPopup/MatchedJobPopup";
import axios from "axios";
import { Search } from "lucide-react";


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
    matching_rate: number;
    hash: string;
}

const DashboardPage = () => {
    const [hasResume, setHasResume] = useState<boolean | null>(null);
    const [selectedJob, setSelectedJob] = useState<MatchedJob | null>(null);
    const [matchedJobs, setMatchedJobs] = useState<MatchedJob[]>([]);
    const [savedJobIds, setSavedJobIds] = useState<string[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const checkResumeExists = async () => {
            try {
                const res = await axios.post(
                    "http://localhost:8001/resume_exists/",
                    {},
                    {
                        headers: {
                            Authorization: `Bearer ${
                                localStorage.getItem("access_token") || ""
                            }`,
                        },
                    }
                );

                setHasResume(res.data.exists);
            } catch (error) {
                console.log("Resume exists check failed:", error);
                setHasResume(false);
            } finally {
                setLoading(false);
            }
        };

        checkResumeExists();
    }, []);

    useEffect(() => {
        if (!hasResume) return;

        const fetchJobs = async () => {
            try {
                const res = await axios.get(
                    "http://localhost:8001/get_relevant_positions/",
                    {
                        headers: {
                            "Content-Type": "application/json",
                            Authorization: `Bearer ${localStorage.getItem("access_token") || ""}`,
                        },
                    }
                );
                setMatchedJobs(res.data);
            } catch (error) {
                console.log(error);
            }
        };


        fetchJobs();
    }, [hasResume]);

    useEffect(() => {
        if (!hasResume) return;

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
                setSavedJobIds(ids);
            } catch (error) {
                console.log(error);
            }
        };

        fetchSavedJobs();
    }, [hasResume]);

    const handleSaveSuccess = (jobId: string) => {
        setSavedJobIds((prev) => [...prev, jobId]);
    };

    if (loading) {
        return <div className={styles.wrapper}>Loading...</div>;
    }

    return (
        <div className={styles.wrapper}>
            {!hasResume ? (
                <NoResumePage />
            ) : (
                <>
                    <div className={styles.content}>
                        <div className={styles.info}>
                            <div>
                                <p className={styles.title}>Your Job Matches</p>
                                <p className={styles.subTitle}>
                                    Personalized recommendations based on your resume and preferences
                                </p>
                            </div>
                            <div className={styles.searchWrapper}>
                                <Search className={styles.searchIcon} size={18}/>
                                <input
                                    type="text"
                                    placeholder="Search jobs..."
                                    className={styles.searchInput}
                                />
                            </div>
                        </div>
                        {matchedJobs.length !== 0 ?
                            (
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
                            ): <h3>There are no jobs that fit your resume.</h3>}

                    </div>

                    {selectedJob && (
                        <MatchedJobPopup
                            job={selectedJob}
                            variant="dashboard"
                            isSaved={savedJobIds.includes(selectedJob.id)}
                            onSave={() => handleSaveSuccess(selectedJob.id)}
                            onClose={() => setSelectedJob(null)}
                        />
                    )}
                </>
            )}
        </div>
    );
};

export default DashboardPage;
