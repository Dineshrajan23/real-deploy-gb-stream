export default function RightSideBar() {
  return (
    <aside className="w-1/4 p-6 bg-gray-800 text-white items-end">
      <h2 className="text-2xl font-bold mb-4">Right Side Bar</h2>
      <p>This is the right sidebar content.</p>
      <ul className="mt-4 space-y-2">
        <li><a href="/link1" className="text-blue-400 hover:underline">Link 1</a></li>
        <li><a href="/link2" className="text-blue-400 hover:underline">Link 2</a></li>
        <li><a href="/link3" className="text-blue-400 hover:underline">Link 3</a></li>
      </ul>
    </aside>
  );
}