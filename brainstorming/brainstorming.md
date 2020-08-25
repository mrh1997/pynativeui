* Ein observable Model ist ein (azyklicher) Baum von datenknoten genannt "Box"
* Jeder datenknoten ist entweder von einem pythonobjekt abgeleitet 
  (falls mutable) oder ein proxy auf ein pythonobjekt (falls immutable)
* Die datenknoten bleiben immer die gleichen objekte, auch wenn sie neu gesetzt
  werden (nach obj.attr = ... zeigt "attr" danach auf das gleiche objekt)
* auf jeden Datenknoten kann ein observer gesetzt werden (diese bleiben
  auch erhalten, wenn der datenknoten mit einem andern wert ersetzt wurde)
   * entweder auf einen bestimmten datenknoten: "@observe(attr[8].subattr)"
   * oder auf eine gruppe von datenknoten: "@observer(attr[ALL].subattr)"
* Wenn ein Datenknoten einem anderen zugewiesen wird, werden sie automatisch
  verlinkt (durch setzen des delegates; ab dann werden alle anfragen 
  weitergeleitet)
* Wenn immutable python objekt einem Datenknoten zugewiesen wird, wird der   
  content des Datenknotens dadurch ersetzt
* Wenn mutable python objekt einem datenknoten zugewiesen wird muss der typ
  passen. Falls ja wird eine Kopier angelegt und dann diese dem content 
  zugewiesen 
* Beim ändern eines Datenknotens wird in folgenden Schritten vorgegangen:
   * Starten einer Transaktion (contextmanager)
   * Sammeln von änderungen
   * Wenn eine exception passiert werden alle Änderungen verworfen
   * Wenn transaktionskontext zu ende werden die gesammelten änderungen
     über die angehängten observer (falls es sich um generatoren handelt) 
     ergänzt.
   * dann werden pro objekt die gesammelten änderung an alle angehängten
     verifier übergeben. Wenn auch nur einer mit exception abbricht werden alle
     Änderungen verworfen. Ggf werden "fixer" funktionen eingesammelt und
     an die exception angehängt. Evtl. auch die Änderungen an die exception
     anhängen, so daß nach durchführung des fixes ein erneuter lauf probiert
     werden kann
   * zum schluss laufen die begonnen generatoren-observer zu ende bzw.
     die nicht-generatoren-observer laufen. Exceptions die hier passieren
     werden abgefangen so das alle observer zu ende laufen können. erst
     danach wird ggf. die erste exception weitergeleitet