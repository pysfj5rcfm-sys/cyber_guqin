export function PhraseStructurePanel() {
  return (
    <div className="phrase-rail">
      <h3>本曲进度概览</h3>
      <div><span>已审 phrase</span><b>12 / 24</b><i style={{ width: "50%" }} /></div>
      <div><span>待审 phrase</span><b>11 / 24</b><i className="gold-line" style={{ width: "46%" }} /></div>
      <div><span>可听版本数</span><b>5 / 5</b><i style={{ width: "100%" }} /></div>
    </div>
  );
}
