export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm lg:flex">
        <h1 className="text-4xl font-bold text-center mb-8">
          SEO Fixer
        </h1>
        <div className="w-full max-w-2xl mx-auto">
          <div className="bg-white p-6 rounded-lg shadow-lg">
            <input
              type="url"
              placeholder="Enter your website URL"
              className="w-full p-3 border border-gray-300 rounded-lg mb-4"
            />
            <button className="w-full bg-primary text-white py-3 px-6 rounded-lg hover:bg-blue-600 transition-colors">
              Analyze My Site
            </button>
          </div>
        </div>
      </div>
    </main>
  )
}
