const features = [
  {
    title: 'Photo to cinematic video',
    description: 'Upload an image and generate a short, motion-driven video with a cinematic look.'
  },
  {
    title: 'Creative prompt control',
    description: 'Describe the motion, mood, and camera direction to produce the exact style you want.'
  },
  {
    title: 'Built for short-form content',
    description: 'Create Reels, ads, promos, and product videos optimized for social platforms.'
  }
];

const steps = [
  'Upload your image',
  'Add prompt and style',
  'Generate your video',
  'Download in seconds'
];

const plans = [
  {
    name: 'Free',
    price: '$0',
    description: 'Perfect to test the product.',
    features: ['3 videos/month', 'Watermarked output', '720p export']
  },
  {
    name: 'Pro',
    price: '$19',
    description: 'Best for creators and freelancers.',
    features: ['Unlimited prompts', 'HD export', 'Commercial use'],
    featured: true
  },
  {
    name: 'Business',
    price: '$49',
    description: 'Built for agencies and marketing teams.',
    features: ['Team workspace', 'Brand kits', 'Priority queue']
  }
];

export default function HomePage() {
  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <section className="mx-auto max-w-7xl px-6 pb-16 pt-10">
        <nav className="mb-12 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-brand-400 to-brand-700 font-bold text-white shadow-glow">
              V
            </div>
            <span className="text-lg font-semibold">VividMotion AI</span>
          </div>
          <div className="hidden items-center gap-8 text-sm text-slate-300 md:flex">
            <a href="#features">Features</a>
            <a href="#how-it-works">How it works</a>
            <a href="#pricing">Pricing</a>
          </div>
          <button className="rounded-full border border-white/20 bg-white/5 px-4 py-2 text-sm font-medium text-white transition hover:bg-white/10">
            Start free
          </button>
        </nav>

        <div className="grid items-center gap-10 lg:grid-cols-[1.2fr_0.8fr]">
          <div>
            <div className="mb-6 inline-flex items-center rounded-full border border-brand-500/30 bg-brand-500/10 px-3 py-1 text-xs font-medium text-brand-200">
              AI image-to-video platform
            </div>

            <h1 className="max-w-xl text-5xl font-black tracking-tight text-white md:text-6xl">
              Turn any image into a cinematic video in seconds.
            </h1>

            <p className="mt-6 max-w-xl text-lg text-slate-300">
              VividMotion AI helps brands, creators, and marketers transform static photos into motion-driven social videos, promos, and product clips without complex editing tools.
            </p>

            <div className="mt-8 flex flex-wrap gap-4">
              <button className="rounded-full bg-brand-500 px-6 py-3 font-semibold text-white transition hover:bg-brand-400">
                Generate a video
              </button>
              <button className="rounded-full border border-white/20 bg-white/5 px-6 py-3 font-semibold text-white transition hover:bg-white/10">
                Watch demo
              </button>
            </div>

            <div className="mt-10 flex items-center gap-8 text-sm text-slate-400">
              <span>5k+ creators</span>
              <span>40k+ videos generated</span>
              <span>4.9/5 user rating</span>
            </div>
          </div>

          <div className="relative">
            <div className="overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-slate-900 to-slate-800 p-4 shadow-2xl shadow-brand-900/40">
              <div className="rounded-2xl bg-gradient-to-br from-brand-500/20 via-slate-900 to-slate-950 p-4">
                <div className="mb-4 flex items-center justify-between text-xs text-slate-300">
                  <span>Original image</span>
                  <span>AI motion</span>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div className="h-64 rounded-2xl bg-[radial-gradient(circle_at_top,_rgba(96,165,250,0.5),_transparent_50%),linear-gradient(135deg,#0f172a,#1e293b_55%,#0f172a)] p-4">
                    <div className="flex h-full items-end justify-start rounded-xl border border-white/10 bg-gradient-to-tr from-slate-900 via-slate-800 to-slate-700 p-3">
                      <div className="h-8 w-16 rounded-full bg-white/10 blur-md" />
                    </div>
                  </div>
                  <div className="h-64 rounded-2xl bg-[radial-gradient(circle_at_top,_rgba(96,165,250,0.5),_transparent_50%),linear-gradient(135deg,#111827,#1f2937_45%,#0f172a)] p-4">
                    <div className="flex h-full items-center justify-center rounded-xl border border-brand-500/40 bg-gradient-to-br from-brand-500/20 to-slate-950">
                      <div className="h-24 w-24 rounded-full border border-brand-200/40 bg-brand-500/10 blur-sm" />
                    </div>
                  </div>
                </div>
                <div className="mt-4 rounded-xl border border-white/10 bg-slate-950/40 p-3 text-xs text-slate-300">
                  <div className="mb-2 flex items-center justify-between">
                    <span>Prompt</span>
                    <span className="text-brand-300">Cinematic zoom</span>
                  </div>
                  <div className="h-2 w-full overflow-hidden rounded-full bg-slate-800">
                    <div className="h-full w-2/3 rounded-full bg-gradient-to-r from-brand-400 to-brand-600" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section id="features" className="mx-auto max-w-7xl px-6 py-20">
        <div className="mb-12 text-center">
          <p className="text-sm font-semibold uppercase tracking-[0.2em] text-brand-300">Why teams use it</p>
          <h2 className="mt-4 text-3xl font-bold text-white md:text-4xl">Everything you need to produce motion content</h2>
        </div>

        <div className="grid gap-6 md:grid-cols-3">
          {features.map((feature) => (
            <div key={feature.title} className="rounded-3xl border border-white/10 bg-white/5 p-6">
              <div className="mb-4 h-12 w-12 rounded-2xl bg-gradient-to-br from-brand-400/30 to-brand-700/30" />
              <h3 className="mb-2 text-xl font-semibold text-white">{feature.title}</h3>
              <p className="text-slate-300">{feature.description}</p>
            </div>
          ))}
        </div>
      </section>

      <section id="how-it-works" className="mx-auto max-w-7xl px-6 py-20">
        <div className="mb-12 text-center">
          <p className="text-sm font-semibold uppercase tracking-[0.2em] text-brand-300">How it works</p>
          <h2 className="mt-4 text-3xl font-bold text-white md:text-4xl">Simple workflow, powerful results</h2>
        </div>

        <div className="grid gap-6 md:grid-cols-4">
          {steps.map((step, idx) => (
            <div key={step} className="rounded-3xl border border-white/10 bg-slate-900 p-6">
              <div className="mb-4 flex h-10 w-10 items-center justify-center rounded-full bg-brand-500/20 text-sm font-bold text-brand-200">
                {idx + 1}
              </div>
              <p className="text-lg font-medium text-white">{step}</p>
            </div>
          ))}
        </div>
      </section>

      <section id="pricing" className="mx-auto max-w-7xl px-6 py-20">
        <div className="mb-12 text-center">
          <p className="text-sm font-semibold uppercase tracking-[0.2em] text-brand-300">Pricing</p>
          <h2 className="mt-4 text-3xl font-bold text-white md:text-4xl">Choose the best plan for your workflow</h2>
        </div>

        <div className="grid gap-6 md:grid-cols-3">
          {plans.map((plan) => (
            <div
              key={plan.name}
              className={`rounded-3xl border p-6 ${
                plan.featured ? 'border-brand-400 bg-brand-500/10 shadow-glow' : 'border-white/10 bg-slate-900'
              }`}
            >
              <div className="mb-4 flex items-center justify-between">
                <h3 className="text-xl font-semibold text-white">{plan.name}</h3>
                {plan.featured && (
                  <span className="rounded-full bg-brand-500 px-2 py-1 text-xs font-medium text-white">Popular</span>
                )}
              </div>
              <p className="mb-4 text-4xl font-black text-white">{plan.price}<span className="text-base text-slate-400">/mo</span></p>
              <p className="mb-6 text-slate-300">{plan.description}</p>
              <ul className="space-y-3 text-sm text-slate-200">
                {plan.features.map((feature) => (
                  <li key={feature}>• {feature}</li>
                ))}
              </ul>
              <button className="mt-8 w-full rounded-full bg-white px-4 py-3 font-semibold text-slate-900 transition hover:bg-slate-200">
                Get started
              </button>
            </div>
          ))}
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-6 pb-24 pt-8">
        <div className="rounded-3xl border border-brand-500/30 bg-gradient-to-r from-brand-500/15 to-sky-500/15 p-8 text-center">
          <h2 className="text-3xl font-bold text-white">Ready to create your first AI-generated video?</h2>
          <p className="mt-4 text-slate-200">Upload an image, add a prompt, and generate a video in minutes.</p>
          <button className="mt-6 rounded-full bg-white px-6 py-3 font-semibold text-slate-900 transition hover:bg-slate-200">
            Start free
          </button>
        </div>
      </section>
    </main>
  );
}
