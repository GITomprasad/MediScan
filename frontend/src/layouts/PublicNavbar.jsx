import React from 'react';
import { NavLink } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Activity, ArrowRight, LayoutDashboard } from 'lucide-react';

const PublicNavbar = () => {
  const { user } = useAuth();

  return (
    <header className="sticky top-0 z-40 bg-white/90 backdrop-blur-md border-b border-slate-200/80">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
        <NavLink to="/" className="flex items-center gap-3 group">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-sky-600 to-cyan-500 flex items-center justify-center text-white shadow-md shadow-sky-500/20 group-hover:scale-105 transition-transform">
            <Activity className="w-6 h-6 stroke-[2.2]" />
          </div>
          <div>
            <div className="flex items-center gap-1.5">
              <span className="font-bold text-xl text-slate-900 tracking-tight">MediScan</span>
              <span className="text-xs font-bold px-1.5 py-0.5 rounded-md bg-sky-100 text-sky-700 tracking-wider">AI</span>
            </div>
            <p className="text-[11px] text-slate-400 font-medium">Medical Report Classification</p>
          </div>
        </NavLink>

        <nav className="hidden md:flex items-center gap-8 text-sm font-medium text-slate-600">
          <a href="#features" className="hover:text-sky-600 transition-colors">Features</a>
          <a href="#how-it-works" className="hover:text-sky-600 transition-colors">How It Works</a>
          <a href="#categories" className="hover:text-sky-600 transition-colors">Categories</a>
          <a href="#architecture" className="hover:text-sky-600 transition-colors">ML Architecture</a>
        </nav>

        <div className="flex items-center gap-3">
          {user ? (
            <NavLink
              to="/dashboard"
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-sky-600 text-white text-sm font-semibold hover:bg-sky-700 shadow-sm transition-all hover:shadow-md"
            >
              <LayoutDashboard className="w-4 h-4" />
              <span>Go to Dashboard</span>
            </NavLink>
          ) : (
            <>
              <NavLink
                to="/login"
                className="px-4 py-2 rounded-xl text-sm font-semibold text-slate-700 hover:text-sky-600 hover:bg-slate-100/70 transition-colors"
              >
                Sign In
              </NavLink>
              <NavLink
                to="/register"
                className="inline-flex items-center gap-1.5 px-4 sm:px-5 py-2.5 rounded-xl bg-gradient-to-r from-sky-600 to-blue-600 text-white text-sm font-semibold hover:from-sky-700 hover:to-blue-700 shadow-sm hover:shadow-md transition-all"
              >
                <span>Get Started</span>
                <ArrowRight className="w-4 h-4" />
              </NavLink>
            </>
          )}
        </div>
      </div>
    </header>
  );
};

export default PublicNavbar;
