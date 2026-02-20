import styles from "./App.module.scss";
import SidePanel from "../components/SidePanel/SidePanel.tsx";
import {Outlet} from "react-router-dom";

function App() {
  return (
    <div className={styles.wrapper}>
      <SidePanel/>
        <div className={styles.content}>
            <Outlet/>
        </div>
    </div>
  )
}

export default App
