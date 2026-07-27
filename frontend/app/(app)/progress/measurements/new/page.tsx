import { MeasurementForm } from "@/components/progress/MeasurementForm";

export default function NewMeasurementPage() {
  return (
    <div className="mx-auto max-w-2xl">
      <h1 className="mb-6 text-2xl font-bold tracking-tight">Log a measurement</h1>
      <MeasurementForm />
    </div>
  );
}
