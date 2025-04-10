import React, { useState, useRef } from "react";
import axios from "axios";

const stylesGallery = Array.from({ length: 16 }, (_, i) => ({
    id: i,
    name: `Style ${i}`,
    image: `/images/${i}.jpg`, 
  }));
  

const ImageStyleForm: React.FC = () => {
  const [image, setImage] = useState<File | null>(null);
  const [style1, setStyle1] = useState<number>(1);
  const [style2, setStyle2] = useState<number | null>(null);
  const [alpha, setAlpha] = useState<number | null>(null);
  const [resultImage, setResultImage] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const fileInputRef = useRef<HTMLInputElement>(null);

  // Handle file selection
  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setImage(file);
    }
  };

  // Handle drag & drop image upload
  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file) {
      setImage(file);
    }
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
  };

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!image) {
      alert("Please select an image.");
      return;
    }

    setLoading(true);
    setResultImage(null); // Reset result image before a new request

    const formData = new FormData();
    formData.append("image", image);
    formData.append("style_1", style1.toString());
    if (style2 !== null) formData.append("style_2", style2.toString());
    if (alpha !== null) formData.append("alpha", alpha.toString());

    try {
      const response = await axios.post("http://localhost:8001/apply-style/", formData, {
        responseType: "blob",
      });
      const imageUrl = URL.createObjectURL(response.data);
      setResultImage(imageUrl);
    } catch (error) {
      console.error("Error applying style:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex w-full mx-auto p-6 bg-white shadow-lg rounded-lg">
      {/* Left Side - Image Upload Form */}
      <div className="w-2/3 pr-6 border-r">
        <h2 className="text-2xl font-semibold mb-4 text-center">Apply Style to Image</h2>

        {/* Drag & Drop Zone */}
        <div
          className="border-2 border-dashed border-gray-300 p-6 text-center cursor-pointer bg-gray-100 rounded-lg hover:bg-gray-200 transition"
          onClick={() => fileInputRef.current?.click()}
          onDrop={handleDrop}
          onDragOver={handleDragOver}
        >
          {image ? (
            <img src={URL.createObjectURL(image)} alt="Uploaded" className="mx-auto h-48 object-cover rounded-lg shadow" />
          ) : (
            <p className="text-gray-500">Drag & drop an image here or click to select</p>
          )}
        </div>

        <input type="file" accept="image/*" ref={fileInputRef} onChange={handleImageChange} className="hidden" />

        {/* Form Inputs */}
        <form onSubmit={handleSubmit} className="space-y-4 mt-4">
          {/* Style 1 Select Dropdown */}
          <select
            value={style1}
            onChange={(e) => setStyle1(Number(e.target.value))}
            className="block w-full border p-2 rounded bg-white"
          >
            {stylesGallery.map((style) => (
              <option key={style.id} value={style.id}>
                {style.name}
              </option>
            ))}
          </select>

          {/* Style 2 (Optional) Select Dropdown */}
          

          {/* Alpha Input */}
          {/* <input
            type="number"
            step="0.1"
            min="0"
            max="1"
            value={alpha ?? ""}
            onChange={(e) => setAlpha(parseFloat(e.target.value))}
            placeholder="Alpha (0-1)"
            className="block w-full border p-2 rounded"
          /> */}

          {/* Submit Button */}
          <button
            type="submit"
            className={`w-full bg-blue-500 text-white py-2 px-4 rounded transition ${loading ? "opacity-50 cursor-not-allowed" : "hover:bg-blue-600"}`}
            disabled={loading}
          >
            {loading ? <span className="animate-pulse">Applying...</span> : "Apply Style"}
          </button>
        </form>

        {/* Transformed Image Preview */}
        {resultImage && !loading && (
          <div className="mt-6 text-center border-t pt-4">
            <h3 className="text-lg font-semibold">Transformed Image</h3>
            <img src={resultImage} alt="Styled Output" className="mt-2 w-full h-auto rounded-lg shadow-lg" />
            <a href={resultImage} download="styled_image.png" className="block mt-2 text-blue-500 underline">
              Download Image
            </a>
          </div>
        )}
      </div>

      {/* Right Side - Styles Gallery */}
      <div className="w-1/3 pl-6">
        <h3 className="text-lg font-semibold mb-3">Available Styles</h3>
        <div className="grid grid-cols-4 gap-3">
          {stylesGallery.map((style) => (
            <div key={style.id} className="text-center">
              <img src={style.image} alt={style.name} className="w-20 h-20 object-cover rounded-lg shadow" />
              <p className="text-xs mt-1">{style.name}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ImageStyleForm;
