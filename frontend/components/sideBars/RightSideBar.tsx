export default function RightSideBar() {
  return (
    <aside className=" bg-zinc-900 text-white p-4 sm:p-6 w-20 sm:w-1/8 flex flex-col items-start sm:items-end ">
      <h2 className="text-sm sm:text-lg text-center bg-gradient-to-r from-purple-600 to-indigo-500 bg-clip-text text-transparent mb-2 sm:mb-4">
        Active Followers
      </h2>

      <ul className="mt-2 sm:mt-4 space-y-1 sm:space-y-2  items-start sm:items-start  ">
        <li>
          <a href="/link1" className="text-xs sm:text-base text-blue-400 hover:underline">
            Link 1
          </a>
        </li>
        <li>
          <a href="/link2" className="text-xs sm:text-base text-blue-400 hover:underline">
            Link 2
          </a>
        </li>
        <li>
          <a href="/link3" className="text-xs sm:text-base text-blue-400 hover:underline">
            Link 3
          </a>
        </li>
      </ul>
    </aside>
  );
}
