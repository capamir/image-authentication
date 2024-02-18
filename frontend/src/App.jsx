import "./App.css";
import Uploader from "./components/Uploader";

function App() {
  return (
    <section className="section">
      <div className="container mx-auto p-5">
        <h1 className="title text-3xl font-bold">Upload Files</h1>
        <Uploader styles="p-16 mt-10 border border-neutral-200" />
      </div>
    </section>
  );
}

export default App;
